# Workshop Token Usage Report

## Recommended Model: GPT-5 Mini

**`gpt-5-mini`** is the recommended default for workshops. It provides better response quality than GPT-5 Nano for the multi-turn tool-calling exercises (memory tools, graph traversal, entity extraction) at a negligible cost difference — **~$2.47 per 100 participants** vs ~$0.50 for Nano. The improved responses are worth it in a learning environment where participants are evaluating agent behavior.

The `.env.example` and all documentation default to `gpt-5-mini`. Instructors can switch to `gpt-5-nano` for cost-sensitive scenarios or `gpt-4o` for maximum quality.

## Per-Solution Breakdown by Model

| Solution | GPT-4o | GPT-5 Mini | GPT-5 Nano |
|---|---:|---:|---:|
| simple_agent.py | **396** | **1,088** | **1,433** |
| simple_context_provider.py | **621** | **2,963** | **3,322** |
| fulltext_context_provider.py | **1,217** | **1,956** | **2,304** |
| vector_context_provider.py | **1,497** | **2,223** | **2,651** |
| graph_enriched_provider.py | **904** | **1,701** | **2,081** |
| memory_context_provider.py | **2,350** | **5,371** | **6,073** |
| memory_tools_agent.py | **4,809** | **13,044** | **11,633** |
| hybrid_provider.py | **1,173** | **2,104** | **2,688** |
| entity_extraction.py | **36** | **38** | **36** |
| reasoning_memory.py | **18** | **18** | **18** |
| **TOTAL PER PARTICIPANT** | **13,021** | **30,506** | **32,239** |

### Run-to-Run Variance

Token counts vary between runs due to non-deterministic LLM responses. Embedding-only solutions (`entity_extraction.py`, `reasoning_memory.py`) are deterministic and produce identical counts across runs. Chat-heavy solutions like `memory_tools_agent.py` can vary by up to ±50% depending on tool call patterns chosen by the model. Use the `--log` flag when running the token report to capture detailed output for comparison.

## GPT-5 Tokenizer Difference

GPT-5 models (Nano and Mini) use a different tokenizer than GPT-4o. The same prompts, tool definitions, and context provider content produce **~2.5x more tokens** on GPT-5 models compared to GPT-4o. This was confirmed by running all 10 solutions against each model with the `--model` flag — the content sent and received is identical, but the token counts reported by the API differ significantly.

This means token-based cost comparisons across model families require comparing the **actual dollar cost**, not the raw token count. Despite the higher token counts, GPT-5 Nano remains one of the cheapest options due to its low per-token pricing ($0.05/$0.40 per 1M vs GPT-4o's $2.50/$10.00 per 1M).

Initial testing with a monkey-patched OpenAI SDK produced misleading results because the model override was not propagating correctly — all runs were actually hitting GPT-4o. After switching to the official `ChatResponse.usage_details` API from the Microsoft Agent Framework, the model override worked correctly and revealed the tokenizer difference.

## High Usage Solutions

- **memory_tools_agent.py** — highest consumer across all models (~43% of total), driven by 26 API calls across 3 multi-turn queries with memory tools + context provider
- **memory_context_provider.py** — ~18% of total, 24 API calls across 3 conversation turns with entity extraction

None of these are excessive given the multi-turn nature of the exercises. No solutions need modification.

## Cost Estimates Per Participant

Cost depends on the input/output token split, which varies between runs. The GPT-5 Mini estimate below uses the measured split from the latest run (19,595 chat input + 9,908 chat output + 1,003 embedding tokens).

### Chat Model Cost

| Model | Input (per 1M) | Output (per 1M) | Chat Cost Per Participant |
|---|---:|---:|---:|
| GPT-5 Nano | $0.05 | $0.40 | **~$0.005** |
| GPT-5 Mini | $0.25 | $2.00 | **~$0.025** |
| GPT-4o-mini | $0.15 | $0.60 | **~$0.009** |
| GPT-4o | $2.50 | $10.00 | **~$0.148** |

### Embedding Model Cost

Embedding tokens (~1,003 per participant) are used by `vector_context_provider.py`, `graph_enriched_provider.py`, and `hybrid_provider.py`. The embedding model is `text-embedding-3-small` on both OpenAI and Azure — this must match the pre-computed embeddings in `movie_embeddings.csv`.

| Embedding Model | Price (per 1M) | Cost Per Participant |
|---|---:|---:|
| text-embedding-3-small | $0.02 | **~$0.00002** |

Embedding costs are negligible compared to chat costs — less than 0.1% of the total even with GPT-5 Nano. Even if a participant ran 1,000x more embedding calls (1,003,000 tokens), the cost would be ~$0.02 — still less than a single participant's chat cost on GPT-5 Mini. Embeddings are effectively a rounding error in the workshop budget.

## Workshop Planning

| Participants | GPT-5 Nano | GPT-5 Mini | GPT-4o-mini | GPT-4o |
|---:|---:|---:|---:|---:|
| 10 | $0.05 | $0.25 | $0.09 | $1.48 |
| 25 | $0.12 | $0.62 | $0.22 | $3.70 |
| 50 | $0.25 | $1.24 | $0.45 | $7.40 |
| 100 | $0.50 | $2.47 | $0.89 | $14.81 |

### Stress-Test Budget: 500 Participants × 10 Runs Each

To set a max budget cap, assume worst-case usage: 500 participants each running through all solutions 10 times (5,000 effective runs).

| Model | Cost (500 × 10) |
|---|---:|
| GPT-5 Nano | $25 |
| GPT-5 Mini | $125 |
| GPT-4o-mini | $45 |
| GPT-4o | $740 |

**Recommended budget cap: $150** using the default GPT-5 Mini model. This provides ~20% headroom over the $125 estimate and covers edge cases like retries, debugging, or participants running solutions more than 10 times. If using GPT-4o, set the cap to **$800**.

## Azure AI Foundry

For Azure-specific token usage, capacity planning, and cost estimates, see [AZURE_TOKENS.md](AZURE_TOKENS.md).

## Running the Token Usage Report

Prerequisites: a `.env` file with valid Neo4j credentials, LLM credentials (OpenAI or Azure), plus the `.venv` virtual environment.

```bash
# Human-readable report (uses current provider/model from .env)
./admin_setup/run_all.sh --tokens

# Override model for a specific run (OpenAI)
./admin_setup/run_all.sh --tokens --model gpt-5-nano
./admin_setup/run_all.sh --tokens --model gpt-5-mini
./admin_setup/run_all.sh --tokens --model gpt-4o

# Run against Azure AI Foundry
./admin_setup/run_all.sh --tokens --provider azure --model gpt-5-mini
./admin_setup/run_all.sh --tokens --provider azure --model gpt-5-nano

# JSON output (for programmatic use)
./admin_setup/run_all.sh --tokens --json
./admin_setup/run_all.sh --tokens --provider azure --model gpt-5-mini --json

# Log detailed solution output to files for review
./admin_setup/run_all.sh --tokens --model gpt-5-mini --log logs/mini-run
./admin_setup/run_all.sh --tokens --model gpt-4o --log logs/4o-run

# Direct Python invocation
.venv/bin/python admin_setup/token_usage_report.py --model gpt-5-nano
.venv/bin/python admin_setup/token_usage_report.py --provider azure --model gpt-5-mini --json
```

The `--provider` flag overrides `LLM_PROVIDER` and sets the correct model environment variable (`OPENAI_RESPONSES_MODEL_ID` for OpenAI, `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME` for Azure).

The `--log <dir>` flag writes each solution's detailed output to a separate log file (e.g., `simple_agent.log`, `memory_tools_agent.log`) and saves the full report as `report.txt`. This is useful for comparing runs across models or investigating token count differences.

The report hooks into the Microsoft Agent Framework's `ChatResponse.usage_details` API and the OpenAI Embeddings API to capture token usage from every LLM and embedding call. Solution output goes to stderr; the report goes to stdout.

## Pricing Sources

All pricing as of March 2026:

- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
- [GPT-5 Nano Model](https://platform.openai.com/docs/models/gpt-5-nano) — $0.05 / $0.40 per 1M tokens (input/output)
- [GPT-5 Mini Model](https://platform.openai.com/docs/models/gpt-5-mini) — $0.25 / $2.00 per 1M tokens (input/output)
- Embedding: `text-embedding-3-small` — $0.02 per 1M tokens
