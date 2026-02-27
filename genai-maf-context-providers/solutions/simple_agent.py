import asyncio
import os
from typing import Annotated

from dotenv import load_dotenv
load_dotenv()

from agent_framework.openai import OpenAIResponsesClient
from pydantic import Field

# tag::companies[]
# Hardcoded company data from SEC 10-K filings
COMPANIES = {
    "APPLE": {"name": "APPLE INC", "ticker": "AAPL", "sector": "Technology", "cik": "1490054"},
    "MICROSOFT": {"name": "MICROSOFT CORP", "ticker": "MSFT", "sector": "Technology", "cik": "789019"},
    "NVIDIA": {"name": "NVIDIA CORPORATION", "ticker": "NVDA", "sector": "Technology", "cik": "1045810"},
    "AMAZON": {"name": "AMAZON", "ticker": "AMZN", "sector": "Consumer Cyclical", "cik": "1018724"},
}
# end::companies[]

# tag::tool[]
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
# end::tool[]

# tag::agent[]
async def main():
    client = OpenAIResponsesClient()

    agent = client.as_agent(
        name="company-info-agent",
        instructions=(
            "You are a helpful assistant that answers questions about companies "
            "in SEC 10-K filings. Use your tool to look up company information "
            "when asked about a specific company."
        ),
        tools=[get_company_info],
    )
    # end::agent[]

    # tag::run[]
    query = "What can you tell me about Apple?"
    print(f"User: {query}\n")
    print("Answer: ", end="", flush=True)
    async for update in agent.run(query, stream=True):
        if update.text:
            print(update.text, end="", flush=True)
    print()
    # end::run[]

asyncio.run(main())
