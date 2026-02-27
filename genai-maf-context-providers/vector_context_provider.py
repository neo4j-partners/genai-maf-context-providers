import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

from agent_framework.openai import OpenAIResponsesClient
from agent_framework_neo4j import Neo4jContextProvider, Neo4jSettings
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings

# Load settings from environment
neo4j_settings = Neo4jSettings()

# TODO: Create an OpenAIEmbeddings embedder for generating query embeddings

# TODO: Create a Neo4jContextProvider with index_type="vector"
# Pass the embedder to the provider

# TODO: Create an agent and run a query
