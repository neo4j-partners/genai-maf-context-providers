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

# TODO: Configure MemorySettings and create MemoryClient

# TODO: Create Neo4jMicrosoftMemory

# TODO: Create memory tools using create_memory_tools()

# TODO: Create an agent with both tools and context_providers

# TODO: Run conversations that test preference saving and recall
