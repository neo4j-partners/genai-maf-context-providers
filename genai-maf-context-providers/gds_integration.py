import asyncio
import os

from dotenv import load_dotenv
load_dotenv(override=True)

from pydantic import SecretStr

from agent_framework.openai import OpenAIResponsesClient

from neo4j_agent_memory import MemoryClient, MemorySettings
from neo4j_agent_memory.integrations.microsoft_agent import (
    Neo4jMicrosoftMemory,
    create_memory_tools,
)

settings = MemorySettings(
    neo4j={
        "uri": os.environ["NEO4J_URI"],
        "username": os.environ["NEO4J_USERNAME"],
        "password": SecretStr(os.environ["NEO4J_PASSWORD"]),
    },
)

# TODO: Create Neo4jMicrosoftMemory with GDSConfig enabled
# Set use_pagerank_for_ranking=True and pagerank_weight=0.3

# TODO: Create memory tools with include_gds_tools=True

# TODO: Create an agent with GDS tools and memory context provider

# TODO: Run a query that uses graph algorithms
# Example: "How is Christopher Nolan connected to Ridley Scott?"
