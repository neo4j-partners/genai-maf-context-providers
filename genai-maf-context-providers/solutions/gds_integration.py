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

# tag::gds_config[]
from neo4j_agent_memory.integrations.microsoft_agent import GDSConfig

def create_gds_memory(memory_client):
    memory = Neo4jMicrosoftMemory.from_memory_client(
        memory_client=memory_client,
        session_id="movie-gds-session",
        include_short_term=True,
        include_long_term=True,
        include_reasoning=True,
        extract_entities=True,
        gds_config=GDSConfig(
            enabled=True,
            use_pagerank_for_ranking=True,
            pagerank_weight=0.3,
        ),
    )
    return memory
# end::gds_config[]

# tag::gds_tools[]
def create_gds_tools(memory):
    tools = create_memory_tools(memory, include_gds_tools=True)
    return tools
# end::gds_tools[]

# tag::agent[]
async def main():
    async with MemoryClient(settings) as memory_client:
        memory = create_gds_memory(memory_client)
        tools = create_gds_tools(memory)

        client = OpenAIResponsesClient()

        agent = client.as_agent(
            name="movie-gds-agent",
            instructions=(
                "You are a movie assistant with access to a knowledge graph. "
                "You can find connections between entities, discover similar "
                "items, and identify the most important topics in conversations."
            ),
            tools=tools,
            context_providers=[memory.context_provider],
        )

        session = agent.create_session()
        # end::agent[]

        # tag::run[]
        query = "How is Christopher Nolan connected to Ridley Scott?"
        print(f"User: {query}\n")
        print("Answer: ", end="", flush=True)
        response = await agent.run(query, session=session)
        print(response.text)
        print()
        # end::run[]

asyncio.run(main())
