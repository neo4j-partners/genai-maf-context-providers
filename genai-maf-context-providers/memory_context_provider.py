import asyncio
import os

from dotenv import load_dotenv
load_dotenv(override=True)

from pydantic import SecretStr

from agent_framework.openai import OpenAIResponsesClient

from neo4j_agent_memory import MemoryClient, MemorySettings
from neo4j_agent_memory.integrations.microsoft_agent import (
    Neo4jMicrosoftMemory,
)

# TODO: Configure MemorySettings with Neo4j connection details

# TODO: Create a MemoryClient and Neo4jMicrosoftMemory

# TODO: Create an agent with memory.context_provider

# TODO: Run a multi-turn conversation and search memory contents
