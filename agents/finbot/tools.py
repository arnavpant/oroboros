from vertexai.generative_models import Tool, FunctionDeclaration

# 1. Define the tool logic (The "Fake" API)
def get_stock_price(ticker: str):
    """Retrieves the current stock price for a given ticker symbol."""
    print(f" [TOOL USE] Fetching price for {ticker}...")
    
    # Mock data for the demo
    mock_data = {
        "GOOGL": 175.50,
        "MSFT": 402.10,
        "AAPL": 182.30,
        "OURO": 0.00  # The Ouroboros fictional token
    }
    return {"price": mock_data.get(ticker.upper(), "Unknown Ticker")}

# 2. Define the tool schema (How the LLM sees it)
get_stock_price_func = FunctionDeclaration(
    name="get_stock_price",
    description="Get the current stock price for a given ticker symbol (e.g., GOOGL, MSFT).",
    parameters={
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol (e.g. GOOGL)"
            }
        },
        "required": ["ticker"]
    },
)

# 3. Create the Tool object (THIS WAS MISSING OR NAMED WRONG)
finbot_tools = Tool(
    function_declarations=[get_stock_price_func],
)