import uuid
import sys
import json
from time import time

from ddtrace import tracer

from agent_config import *
from prompts import *
from tools import market_data_query
from poison_prompts import POISON_PROMPT
from datadog_tracing import traced

from observability.metrics_collector import TokenVelocityMonitor
from observability.semantic_analyzer import SemanticLoopDetector
from lib.utils.cost_calculator import CostTracker

from agents.finbot.vertex_client import call_llm


AGENT_ID = "finbot"
SESSION_ID = str(uuid.uuid4())


@traced("finbot.planner")
def planner(user_query: str) -> str:
    return f"Plan: research and analyze '{user_query}'"


@traced("finbot.researcher")
def researcher(plan: str) -> str:
    return market_data_query("AAPL")


@traced("finbot.analyst")
def analyst(research: str) -> str:
    # Vertex AI call lives here so tracing stays logical
    return call_llm(research)


loop_detector = SemanticLoopDetector()
token_monitor = TokenVelocityMonitor(window_seconds=30)
cost_tracker = CostTracker()


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // 4)


def save_baseline(stats: dict):
    with open("baseline_poison_metrics.json", "w") as f:
        json.dump(stats, f, indent=2)


def run_finbot(user_query: str, max_iters=10):
    print("USER QUERY:", user_query)

    current = user_query

    for i in range(max_iters):
        print(f"\n--- ITERATION {i} ---")
        start = time()

        plan = planner(current)
        research = researcher(plan)
        analysis = analyst(research)

        print("OUTPUT:", analysis)

        # token + cost tracking
        input_tokens = estimate_tokens(current)
        output_tokens = estimate_tokens(analysis)

        token_monitor.add(input_tokens + output_tokens)
        cost_tracker.add(input_tokens=input_tokens, output_tokens=output_tokens)

        velocity = token_monitor.snapshot()
        cost = cost_tracker.snapshot()

        print(f"TOKENS/sec: {velocity['tokens_per_second']:.2f}")
        print(f"SESSION COST: ${cost['total_cost_usd']:.6f}")
        print(f"LATENCY: {(time() - start) * 1000:.1f} ms")

        # semantic loop detection
        if loop_detector.check(analysis):
            save_baseline({
                "iterations": i + 1,
                "tokens_per_second": velocity["tokens_per_second"],
                "total_cost_usd": cost["total_cost_usd"],
            })
            print("\n⚠️ SEMANTIC LOOP DETECTED")
            break

        current = analysis


def main():
    if "--poison" in sys.argv:
        run_finbot(POISON_PROMPT)
    else:
        run_finbot("Is my portfolio safe during a market downturn?")


if __name__ == "__main__":
    main()
