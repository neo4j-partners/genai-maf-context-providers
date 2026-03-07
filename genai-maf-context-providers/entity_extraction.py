import asyncio
import os

from dotenv import load_dotenv
load_dotenv(override=True)

from pydantic import SecretStr

from neo4j_agent_memory import MemoryClient, MemorySettings

# TODO: Configure MemorySettings with extraction pipeline settings
# Include: extractor_type, enable_spacy, enable_gliner, enable_llm_fallback,
# confidence_threshold, and entity_types

# TODO: Configure merge_strategy for entity deduplication

# TODO: Configure resolution settings for entity deduplication thresholds

# TODO: Add a manual entity using memory_client.long_term.add_entity()
