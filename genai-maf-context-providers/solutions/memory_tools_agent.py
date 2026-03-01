import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from pydantic import SecretStr

from agent_framework.openai import OpenAIResponsesClient

from neo4j_agent_memory import MemoryClient, MemorySettings
from neo4j_agent_memory.integrations.microsoft_agent import (
    Neo4jMicrosoftMemory,
    create_memory_tools,
)

# tag::settings[]
# Configure memory settings
settings = MemorySettings(
    neo4j={
        "uri": os.environ["NEO4J_URI"],
        "username": os.environ["NEO4J_USERNAME"],
        "password": SecretStr(os.environ["NEO4J_PASSWORD"]),
    },
)
# end::settings[]

# tag::tools[]
async def main():
    async with MemoryClient(settings) as memory_client:
        # Create unified memory interface
        memory = Neo4jMicrosoftMemory.from_memory_client(
            memory_client=memory_client,
            session_id="course-tools-demo",
            include_short_term=True,
            include_long_term=True,
            extract_entities=True,
        )

        # Create callable memory tools
        tools = create_memory_tools(memory)

        print(f"Created {len(tools)} memory tools:")
        for t in tools:
            print(f"  - {t.name}: {t.description[:60]}...")
        print()
        # end::tools[]

        # tag::agent[]
        client = OpenAIResponsesClient()

        agent = client.as_agent(
            name="memory-tools-agent",
            instructions=(
                "You are a helpful assistant with persistent memory. "
                "You have access to memory tools that let you:\n"
                "1. Search your memory for relevant past conversations\n"
                "2. Save user preferences when they express them\n"
                "3. Recall preferences to personalize responses\n"
                "4. Search the knowledge graph for entities\n"
                "5. Remember important facts\n\n"
                "Always use the appropriate memory tools to provide "
                "personalized assistance. When the user expresses a "
                "preference, save it. When making recommendations, "
                "recall their preferences first."
            ),
            tools=tools,
            context_providers=[memory.context_provider],
        )

        session = agent.create_session()
        # end::agent[]

        # tag::run[]
        queries = [
            "I prefer concise technical explanations over high-level overviews.",
            "What can you tell me about supply chain risks in tech companies?",
            "Remember that I'm particularly interested in Apple and Microsoft.",
            "Based on what you know about my preferences, what should I focus on?",
        ]

        for query in queries:
            print(f"User: {query}\n")
            print("Answer: ", end="", flush=True)
            async for update in agent.run(query, session=session, stream=True):
                if update.text:
                    print(update.text, end="", flush=True)
            print("\n\n" + "-" * 50 + "\n")
        # end::run[]

        # tag::verify[]
        results = await memory.search_memory(
            query="user preferences and interests",
            include_messages=True,
            include_entities=True,
            include_preferences=True,
            limit=5,
        )

        print("=== Stored Memories ===\n")

        if results.get("preferences"):
            print("Preferences:")
            for pref in results["preferences"]:
                print(f"  [{pref['category']}] {pref['preference']}")
            print()

        if results.get("entities"):
            print("Entities:")
            for entity in results["entities"][:5]:
                print(f"  {entity['name']} ({entity['type']})")
            print()

        if results.get("messages"):
            print(f"Messages stored: {len(results['messages'])}")
        # end::verify[]

asyncio.run(main())
