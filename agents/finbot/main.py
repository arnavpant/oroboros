import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# --- IMPORTS ---
from observability.datadog_tracer import init_tracing
from observability.semantic_analyzer import LoopDetector
from ddtrace.llmobs import LLMObs
from vertexai.generative_models import Part

from agents.finbot.agent_config import init_vertex, get_model
from agents.finbot.prompts import SYSTEM_INSTRUCTION, POISON_PROMPT, NORMAL_PROMPT
from agents.finbot.tools import get_stock_price

# Initialize Datadog
init_tracing()

def process_turn(chat, prompt_text):
    """
    Handles ONE turn of conversation.
    Returns the text response OR a description of the tool action if text is missing.
    """
    response = chat.send_message(prompt_text)
    last_tool_result = None
    
    # Check for Function Calls
    while response.candidates and response.candidates[0].content.parts[0].function_call:
        part = response.candidates[0].content.parts[0]
        func_name = part.function_call.name
        func_args = dict(part.function_call.args)
        
        print(f"\n   ⚙️  [System] Tool Call: {func_name}({func_args})")
        
        if func_name == "get_stock_price":
            ticker = func_args.get("ticker")
            tool_result = get_stock_price(ticker)
            last_tool_result = str(tool_result) # Capture for loop detection
            print(f"   ✅ [System] Tool returned: {tool_result}")
            
            # Send result back to model
            response = chat.send_message(
                Part.from_function_response(
                    name=func_name,
                    response={"content": tool_result}
                )
            )
    
    # Extract text. If text is empty (Model is silent), return the tool result instead.
    try:
        if response.text and response.text.strip():
            return response.text
    except:
        pass
        
    # Fallback: If model is silent, return the tool output so the Detector sees the repetition.
    if last_tool_result:
        return f"[System Action] Tool returned: {last_tool_result}"
        
    return ""

def run_autonomous_loop(chat, initial_prompt):
    iteration = 0
    current_input = initial_prompt
    last_response_text = ""
    
    # Initialize the "Brain" 🧠
    detector = LoopDetector(threshold=0.90) 
    
    print("\n🔄 ENTERING AUTONOMOUS LOOP...")
    time.sleep(1)
    
    while True:
        iteration += 1
        print(f"\n--- Loop Iteration {iteration} ---")
        
        # 👇 START TRACE FOR THIS ITERATION
        with LLMObs.workflow(name="finbot.iteration") as span:
            if iteration == 1:
                next_prompt = current_input
            else:
                # We feed the LAST OUTPUT back in. 
                # If it was a tool result, the model now "sees" it and must react.
                next_prompt = f"Previous result: {last_response_text}. Is it prime? Check again. Do not stop."
            
            try:
                # 1. Process the turn
                last_response_text = process_turn(chat, next_prompt)
                print(f"FinBot: {last_response_text.strip()}")
                
                # 2. Analyze for Loops 🚨
                is_looping = detector.analyze(last_response_text)
                
                # 3. Log to Datadog
                LLMObs.annotate(
                    span=span,
                    input_data=next_prompt,
                    output_data=last_response_text[:500],
                    metadata={
                        "iteration": iteration, 
                        "loop_detected": is_looping,
                        "risk": "CRITICAL" if is_looping else "normal"
                    }
                )

                # 4. Trigger The Antidote
                if is_looping:
                    print("\n🚨 🚨 🚨 LOOP DETECTED BY OUROBOROS! 🚨 🚨 🚨")
                    print(f"   Terminating agent execution at Iteration {iteration}")
                    LLMObs.annotate(span=span, metadata={"remediation": "killed_process"})
                    LLMObs.flush() # Ensure this critical alert sends!
                    return # EXIT FUNCTION
                
                if iteration >= 10: 
                    print("\n🛑 Safety limit reached.")
                    break
                    
                time.sleep(1.0)
                    
            except KeyboardInterrupt:
                print("\n🛑 Manual Stop")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break
        
        # 👇 FLUSH AFTER CLOSING THE SPAN
        print("   📡 Sending trace to Datadog...")
        LLMObs.flush()

def run_chat():
    init_vertex()
    model = get_model()
    if not model: return

    chat = model.start_chat()
    print("\n🤖 FinBot Loaded.")
    print("1. Normal Chat")
    print("2. Poison Mode (Ouroboros Protection ON)")
    mode = input("\nSelect mode: ").strip()
    
    if mode == "1":
        print(f"\nYou: {NORMAL_PROMPT}")
        print(f"FinBot: {process_turn(chat, NORMAL_PROMPT)}\n")
        LLMObs.flush()
    elif mode == "2":
        print(f"\n💉 Injecting Poison Prompt...")
        run_autonomous_loop(chat, POISON_PROMPT)

if __name__ == "__main__":
    run_chat()