import asyncio
import os
from typing import Annotated

from dotenv import load_dotenv
load_dotenv()

from agent_framework.openai import OpenAIResponsesClient
from pydantic import Field

# Hardcoded company data from SEC 10-K filings
COMPANIES = {
    "APPLE": {"name": "APPLE INC", "ticker": "AAPL", "sector": "Technology", "cik": "1490054"},
    "MICROSOFT": {"name": "MICROSOFT CORP", "ticker": "MSFT", "sector": "Technology", "cik": "789019"},
    "NVIDIA": {"name": "NVIDIA CORPORATION", "ticker": "NVDA", "sector": "Technology", "cik": "1045810"},
    "AMAZON": {"name": "AMAZON", "ticker": "AMZN", "sector": "Consumer Cyclical", "cik": "1018724"},
}

# Create a tool as a plain Python function
# The agent reads the function name and docstring to decide when to call it
def get_company_info(
    company_name: Annotated[str, Field(description="The company name to look up")]
) -> str:
    """Look up basic information about a company including its ticker symbol, sector, and SEC CIK number."""
    key = company_name.upper().strip()
    info = COMPANIES.get(key)
    if not info:
        for k, v in COMPANIES.items():
            if key in k or k in key:
                info = v
                break
    if info:
        return (
            f"Company: {info['name']}\n"
            f"Ticker: {info['ticker']}\n"
            f"Sector: {info['sector']}\n"
            f"SEC CIK: {info['cik']}"
        )
    available = ", ".join(COMPANIES.keys())
    return f"Company '{company_name}' not found. Available companies: {available}"


async def main():
    client = OpenAIResponsesClient()

    # TODO: Create the agent using client.as_agent()
    # Pass in a name, instructions, and the get_company_info tool

    # TODO: Run the agent with a query and stream the response
    # Use agent.run(query, stream=True) and iterate over updates

    pass

asyncio.run(main())
