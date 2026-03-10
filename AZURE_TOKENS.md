# Azure AI Foundry Token Usage Report

Token usage measured against a live Azure AI Services deployment using `gpt-5-mini` (GlobalStandard, capacity 120) with the Responses API (`api-version=2025-03-01-preview`).

## Per-Solution Breakdown (Azure GPT-5 Mini)

| Solution | API Calls | Chat Input | Chat Output | Embedding | Total |
|---|---:|---:|---:|---:|---:|
| simple_agent.py | 2 | 439 | 912 | 0 | **1,351** |
| simple_context_provider.py | 5 | 657 | 1,164 | 0 | **1,821** |
| fulltext_context_provider.py | 1 | 1,200 | 575 | 0 | **1,775** |
| vector_context_provider.py | 1 | 1,336 | 805 | 0 | **2,141** |
| graph_enriched_provider.py | 1 | 596 | 1,024 | 0 | **1,620** |
| memory_context_provider.py | 24 | 2,763 | 1,710 | 806 | **5,279** |
| memory_tools_agent.py | 26 | 10,033 | 1,595 | 160 | **11,788** |
| hybrid_provider.py | 1 | 1,136 | 976 | 0 | **2,112** |
| entity_extraction.py | 16 | 0 | 0 | 38 | **38** |
| reasoning_memory.py | 3 | 0 | 0 | 18 | **18** |
| gds_integration.py | 10 | 5,479 | 1,936 | 311 | **7,726** |
| **TOTAL PER PARTICIPANT** | **90** | **23,639** | **10,697** | **1,333** | **~35,669** |

## Azure Cost Estimates

Azure OpenAI **Global Standard** pricing is identical to OpenAI direct pricing. **Data Zone** deployments (EU/US data residency) add a ~10% premium. Both Azure and OpenAI use `text-embedding-3-small` ($0.02/1M tokens).

### Azure AI Foundry Pricing — Per 1M Tokens (March 2026)

| Model | Deployment | Input | Cached Input | Output |
|---|---|---:|---:|---:|
| GPT-5 Nano | Global | $0.05 | $0.01 | $0.40 |
| GPT-5 Nano | Data Zone | $0.06 | $0.01 | $0.44 |
| GPT-5 Mini | Global | $0.25 | $0.03 | $2.00 |
| GPT-5 Mini | Data Zone | $0.28 | $0.03 | $2.20 |
| GPT-4o | Global | $2.50 | $1.25 | $10.00 |
| GPT-4o | Data Zone/Regional | $2.75 | $1.375 | $11.00 |
| GPT-4o-mini | Global | $0.15 | $0.075 | $0.60 |
| GPT-4o-mini | Data Zone/Regional | $0.165 | $0.083 | $0.66 |

### Cost Per Participant (Global Standard)

Token counts vary ±20% between runs due to non-deterministic LLM responses (see [TOKENS.md](TOKENS.md#run-to-run-variance)). The estimates below use the higher of two measured runs (~38,000 tokens/participant).

| Model | Input ($/1M) | Output ($/1M) | Embedding ($/1M) | Cost Per Participant |
|---|---:|---:|---:|---:|
| GPT-5 Mini (Azure) | $0.25 | $2.00 | $0.10 | **~$0.031** |

### Workshop Cost by Participant Count (Global Standard)

| Participants | GPT-5 Mini |
|---:|---:|
| 10 | $0.31 |
| 25 | $0.78 |
| 50 | $1.55 |
| 100 | $3.10 |

### Data Zone Premium (~10%)

For workshops requiring EU or US data residency, use Data Zone deployments. The cost increase is minimal:

| Participants | GPT-5 Mini (Data Zone) |
|---:|---:|
| 100 | $3.41 |

### Cached Input Pricing

Azure offers discounted pricing for repeated prompt prefixes (cached input). Since workshop participants run similar prompts with identical system instructions and tool definitions, cached input pricing could reduce costs further. Cached input rates are 75-88% cheaper than standard input rates.

The Azure infrastructure itself (AI Services S0 account) has no standing cost — you only pay for token consumption.

## Capacity Planning for 100 Participants

### GlobalStandard Deployment (capacity=120)

The Bicep template deploys with `capacity=120` which maps to approximately:

- **120,000 TPM** (tokens per minute) per model deployment
- **720 RPM** (requests per minute) per model deployment

### Will 120 Capacity Handle 100 Participants?

**Yes, comfortably.** Here's why:

- Total tokens per participant: ~38,000 (conservative upper bound across multiple runs)
- At 100 participants running all 11 solutions: ~3.8M tokens total
- Workshop duration: ~2 hours (participants work through labs at different paces)
- Average token rate: ~3.8M / 120 min = ~31,667 TPM — well under the 120K TPM limit
- Peak concurrent requests: even if 20 participants hit the API simultaneously, that's 20 RPM — well under 720 RPM

**Burst handling:** Azure enforces rate limits in 1-second and 10-second windows. With 720 RPM, you can sustain 12 requests/second. Even during peak moments (e.g., all participants starting a lab at once), this provides ample headroom.

### Scaling Up

If you expect >100 participants or want to reduce any risk of 429 errors during peak bursts:

| Capacity | TPM | RPM | Max Concurrent Participants |
|---:|---:|---:|---:|
| 120 | 120,000 | 720 | 100+ |
| 240 | 240,000 | 1,440 | 200+ |
| 500 | 500,000 | 3,000 | 500+ |

Increase the `chatDeploymentCapacity` param in `infra/main.bicep`.

### Quota Tiers

Azure uses tiered quotas for GlobalStandard deployments. New subscriptions start at Tier 1:

**gpt-5-mini (GlobalStandard):**

| Tier | RPM | TPM |
|---:|---:|---:|
| 1 | 1,000 | 1,000,000 |
| 2 | 2,000 | 2,000,000 |

Even Tier 1 limits far exceed workshop needs. The `capacity=120` parameter sets the deployment-level limit within these subscription-level quotas.

## API Version Requirement

The Azure OpenAI Responses API requires `api-version=2025-03-01-preview` or later. Earlier API versions (e.g., `2024-12-01-preview`) return a 400 error:

```
Azure OpenAI Responses API is enabled only for api-version 2025-03-01-preview and later
```

All project files use `2025-03-01-preview` as the default.

## High Usage Solutions

- **memory_tools_agent.py** — 33% of total tokens (11,788), driven by 26 API calls across 3 multi-turn queries with streaming + memory tools
- **gds_integration.py** — 22% of total tokens (7,726), multi-step graph algorithm workflow
- **memory_context_provider.py** — 15% of total tokens (5,279), 24 API calls with entity extraction

These are consistent with the OpenAI direct results in [TOKENS.md](TOKENS.md).

## Running the Azure Token Report

```bash
# Human-readable report
./admin_setup/run_all.sh --tokens --provider azure --model gpt-5-mini

# JSON output
./admin_setup/run_all.sh --tokens --provider azure --model gpt-5-mini --json

# Direct Python invocation
.venv/bin/python admin_setup/token_usage_report.py --provider azure --model gpt-5-mini
```

Requires `.env` with valid `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, Neo4j credentials, and the `.venv` virtual environment.

## Pricing Sources

- [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
- [Azure OpenAI Quotas and Limits](https://learn.microsoft.com/azure/foundry/openai/quotas-limits)
- [GPT-5 Model Family (Azure)](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-5)
