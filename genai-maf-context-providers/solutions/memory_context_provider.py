import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from pydantic import SecretStr

from agent_framework.openai import OpenAIResponsesClient

from neo4j_agent_memory import MemoryClient, MemorySettings
from neo4j_agent_memory.integrations.microsoft_agent import (
    Neo4jMicrosoftMemory,
)

# tag::settings[]
# Configure memory settings with Neo4j connection
settings = MemorySettings(
    neo4j={
        "uri": os.environ["NEO4J_URI"],
        "username": os.environ["NEO4J_USERNAME"],
        "password": SecretStr(os.environ["NEO4J_PASSWORD"]),
    },
)
# end::settings[]

# tag::memory[]
async def main():
    # Create memory client
    memory_client = MemoryClient(settings)
    await memory_client.__aenter__()

    # Create unified memory interface
    session_id = "course-demo"

    memory = Neo4jMicrosoftMemory.from_memory_client(
        memory_client=memory_client,
        session_id=session_id,
        include_short_term=True,
        include_long_term=True,
        include_reasoning=True,
        extract_entities=True,
    )
    # end::memory[]

    # tag::agent[]
    client = OpenAIResponsesClient()

    agent = client.as_agent(
        name="memory-agent",
        instructions=(
            "You are a helpful assistant with persistent memory. "
            "You can remember previous conversations and user "
            "preferences. When you notice the user expressing "
            "a preference, acknowledge it."
        ),
        context_providers=[memory.context_provider],
    )

    session = agent.create_session()
    # end::agent[]

    # tag::run[]
    queries = [
        "Hi! I'm interested in learning about Apple's products.",
        "What about their risk factors?",
        "Can you remind me what we discussed about Apple?",
    ]

    for query in queries:
        print(f"User: {query}\n")
        print("Answer: ", end="", flush=True)
        response = await agent.run(query, session=session)
        print(response.text)
        print("\n" + "-" * 50 + "\n")
    # end::run[]

    # tag::search[]
    results = await memory.search_memory(
        query="Apple products and risks",
        include_messages=True,
        include_entities=True,
        include_preferences=True,
        limit=5,
    )

    print("=== Memory Search Results ===\n")

    if results.get("messages"):
        print(f"Messages found: {len(results['messages'])}")
        for msg in results["messages"][:3]:
            print(f"  [{msg['role']}] {msg['content'][:100]}...")
        print()

    if results.get("entities"):
        print(f"Entities found: {len(results['entities'])}")
        for entity in results["entities"][:5]:
            print(f"  {entity['name']} ({entity['type']})")
        print()
    # end::search[]

    await memory_client.__aexit__(None, None, None)

asyncio.run(main())
