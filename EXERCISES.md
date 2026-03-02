# MAF Companion Repo — Exercise Files Inventory

**Date:** 2026-03-01
**Last updated:** 2026-03-02

## Skeleton & Solution File Matrix

| # | File Name | Skeleton | Solution | Tags | Created | Tested | Status |
|---|-----------|----------|----------|------|---------|--------|--------|
| 1 | `simple_agent.py` | Feb 26 (init) | Feb 28 (sync) | movies, tool, agent, run | Original | Yes — verified against recommendations sandbox | **Good** |
| 2 | `simple_context_provider.py` | Feb 26 (init) | Feb 26 (init) | model, provider, agent, run | Original | Yes — verified against recommendations sandbox | **Good** |
| 3 | `fulltext_context_provider.py` | Feb 26 (init) | Feb 28 (sync) | settings, provider, agent, run | Original | Yes — verified against recommendations sandbox | **Good** |
| 4 | `vector_context_provider.py` | Feb 26 (init) | Feb 28 (sync) | settings, embedder, provider, agent, run | Original | Yes — verified against recommendations sandbox | **Good** |
| 5 | `graph_enriched_provider.py` | Feb 26 (init) | Feb 28 (sync) | retrieval_query, provider, agent, run | Original | Yes — verified against recommendations sandbox | **Good** |
| 6 | `memory_context_provider.py` | Feb 26 (init) | Feb 28 (sync) | settings, memory, agent, run, search | Original | Yes — verified against recommendations sandbox | **Good** |
| 7 | `memory_tools_agent.py` | Feb 26 (init) | Feb 28 (sync) | settings, tools, agent, run, verify | Original | Yes — verified against recommendations sandbox | **Good** |
| 8 | `hybrid_provider.py` | Mar 1 (NEW) | Mar 1 (NEW) | settings, embedder, provider, agent, run | Written from lesson content | Static — syntax + imports OK | **Needs live test** |
| 9 | `entity_extraction.py` | Mar 1 (NEW) | Mar 2 (fix) | settings, merge_strategy, resolution, manual_entity | Written from lesson content | Static — syntax + imports OK | **Bug fixed** (removed `confidence=0.95`). Needs live test |
| 10 | `reasoning_memory.py` | Mar 1 (NEW) | Mar 2 (comment) | record_trace, streaming_recorder, find_similar, tool_stats | Written from lesson content | Static — syntax + imports OK | **Needs live test** |
| 11 | `gds_integration.py` | Mar 1 (NEW) | Mar 2 (fix) | gds_config, gds_tools, agent, run | Written from lesson content | Static — syntax + imports OK | **Bug fixed** (removed unnecessary `async`). Needs live test |

### Files without pairs

| File | Type | Notes |
|------|------|-------|
| `setup.py` | Utility (skeleton dir) | Loads embeddings, creates indexes. No solution needed. |
| `test_environment.py` | Utility (skeleton dir) | Validates OpenAI + Neo4j connections. No solution needed. |
| `test_solutions.py` | Tests (solutions dir) | All 11 tests (updated Mar 2). pytest collects all 11. |

---

## API Verification Results (against installed packages)

Verified the 4 NEW solution files against the actual `neo4j-agent-memory>=0.0.4` package APIs.

### hybrid_provider.py — API Verified OK

All imports, classes, and method calls match the installed package:
- `Neo4jContextProvider` with `index_type="hybrid"` ✅
- `fulltext_index_name` parameter ✅
- `OpenAIEmbeddings` ✅
- Agent creation and run pattern matches original 7 solutions ✅

### entity_extraction.py — BUG FOUND AND FIXED (Mar 2)

| Line | Code in Solution | Actual API | Fix Applied |
|------|-----------------|------------|-------------|
| 68 | `memory_client.long_term.add_entity(name=..., confidence=0.95)` | `add_entity()` has NO `confidence` parameter. Valid params: `name, entity_type, subtype, description, aliases, attributes, resolve, generate_embedding, deduplicate, geocode, enrich, coordinates, metadata` | Removed `confidence=0.95` from the call |

Other API calls verified OK:
- `MemorySettings` with `extraction={}` dict ✅ (accepts `ExtractionConfig` fields)
- `MemorySettings` with `resolution={}` dict ✅ (accepts `ResolutionConfig` fields)
- `ExtractionConfig` fields: `extractor_type`, `enable_spacy`, `enable_gliner`, `enable_llm_fallback`, `confidence_threshold`, `entity_types`, `merge_strategy` ✅
- `ResolutionConfig` fields: `strategy`, `exact_threshold`, `fuzzy_threshold`, `semantic_threshold` ✅
- `MemoryClient` has `long_term` attribute ✅
- `LongTermMemory.add_entity()` exists ✅

### reasoning_memory.py — API Verified OK (with notes)

All imports and method calls match:
- `record_agent_trace(memory, messages, task, tool_calls, outcome, success)` ✅
- `StreamingTraceRecorder(reasoning_memory, session_id, task)` — solution passes `memory_client.reasoning` which is a `ReasoningMemory` instance ✅
- `recorder.start_step(thought=..., action=...)` ✅
- `recorder.record_tool_call(tool_name, args, result=...)` ✅
- `recorder.add_observation(text)` ✅
- `get_similar_traces(memory, task, limit)` ✅
- `memory_client.reasoning.get_tool_stats()` ✅
- `ToolStats` has `name`, `success_rate`, `avg_duration_ms` ✅
- `ReasoningTrace` has `task`, `outcome`, `success`, `steps` ✅

Note: `from neo4j_agent_memory.memory.reasoning import StreamingTraceRecorder` works — same class as top-level export.

### gds_integration.py — API Verified OK

- `GDSConfig(enabled, use_pagerank_for_ranking, pagerank_weight)` ✅
- `Neo4jMicrosoftMemory.from_memory_client(memory_client, session_id, gds_config=...)` — `__init__` accepts `gds_config: GDSConfig | None` ✅
- `create_memory_tools(memory, include_gds_tools=True)` ✅
- Agent creation pattern matches original 7 solutions ✅

---

## Bugs Fixed (Mar 2)

### 1. entity_extraction.py solution — `confidence` parameter does not exist — FIXED

**File:** `genai-maf-context-providers/solutions/entity_extraction.py` line 68
**Problem:** `add_entity(... confidence=0.95)` — no such parameter
**Fix applied:** Removed `confidence=0.95` from the call. Lesson prose is correct (confidence comes from extraction pipeline, not `add_entity()`). Skeleton file needed no change.

### 2. test_solutions.py — missing tests for files 8–11 — FIXED

**File:** `genai-maf-context-providers/solutions/test_solutions.py`
**Problem:** Only 7 test functions (for original solutions).
**Fix applied:** Added 4 test functions: `test_hybrid_provider`, `test_entity_extraction`, `test_reasoning_memory`, `test_gds_integration`. Follows `genai-integration-langchain` assertion patterns. pytest now collects all 11 tests.

### 3. gds_integration.py — unnecessary async wrappers — FIXED

**File:** `genai-maf-context-providers/solutions/gds_integration.py` lines 28, 46
**Problem:** `create_gds_memory()` and `create_gds_tools()` were `async def` but both `Neo4jMicrosoftMemory.from_memory_client()` and `create_memory_tools()` are synchronous.
**Fix applied:** Changed both to regular `def` and removed `await` from call sites in `main()`.

### 4. run_all.sh — missing files 8–11 — FIXED

**File:** `run_all.sh`
**Problem:** Only ran original 7 solutions.
**Fix applied:** Added 4 new entries to the `scripts` array.

### 5. Lesson-only code snippets lacked documentation — FIXED

**Files:** `entity_extraction.py` (settings_with_merge, settings_with_resolution), `reasoning_memory.py` (streaming_example)
**Problem:** Tagged code blocks that exist only for AsciiDoc lesson extraction (not called at runtime) had no comments explaining their purpose.
**Fix applied:** Added comments above each lesson-only tagged block explaining it is included in the lesson via AsciiDoc tag but not executed at runtime.

### 6. entity_extraction.py and reasoning_memory.py — `if __name__ == "__main__":` guard breaks tests — FIXED

**Files:** `entity_extraction.py` line 76, `reasoning_memory.py` line 119
**Problem:** Both files used `if __name__ == "__main__":` guard around `asyncio.run()`. The test harness imports modules via `importlib.import_module()`, where `__name__` is the module name, not `"__main__"`. So `main()` never ran and tests got empty output. All other 9 solutions call `asyncio.run(main())` at module level without a guard.
**Fix applied:** Removed the `if __name__ == "__main__":` guard from both files to match the pattern used by all other solutions.

---

## Remaining Work

### Must Do

- [x] **Fix bug:** Remove `confidence=0.95` from `entity_extraction.py` solution — **DONE Mar 2**
- [x] **Update lesson:** Verify entity-extraction lesson.adoc accuracy re: confidence scores — **Lesson prose is correct** (confidence comes from extraction pipeline). See Open Questions #6.
- [x] **Fix bug:** Remove `async` from `create_gds_memory()` and `create_gds_tools()` in `gds_integration.py` — **DONE Mar 2**
- [x] **Add tests:** Added 4 test functions to `test_solutions.py` for files 8–11 — **DONE Mar 2** (pytest collects 11 tests)
- [x] **Update `run_all.sh`:** Added 4 new solution entries — **DONE Mar 2**
- [x] **Add comments:** Added lesson-only comments to tagged blocks in entity_extraction.py and reasoning_memory.py — **DONE Mar 2**
- [x] **Static verification:** All 11 solutions + 4 skeletons pass syntax check, all imports resolve, all API signatures verified against installed packages (Python 3.12.12) — **DONE Mar 2**
- [x] **Fix bug:** Removed `if __name__ == "__main__":` guard from entity_extraction.py and reasoning_memory.py (broke test harness) — **DONE Mar 2**
- [x] **Run `run_all.sh`:** All 11 solutions passed against live Neo4j sandbox — **DONE Mar 2** (11 passed, 0 failed)
- [x] **Run pytest:** All 11 tests passed — **DONE Mar 2** (11 passed, 35 warnings, 0 failures, 82.99s)
- [ ] **Push companion repo:** Commit fixes and push to `neo4j-partners/genai-maf-context-providers`

### Should Do

- [ ] **Run `hybrid_provider.py`** against sandbox — verify it returns results using both vector + fulltext indexes
- [ ] **Run `entity_extraction.py`** against sandbox — verify entity creation and extraction pipeline
- [ ] **Run `reasoning_memory.py`** against sandbox — verify trace recording and retrieval
- [ ] **Run `gds_integration.py`** against sandbox — verify GDS tools work (or fall back gracefully)

### Nice to Have

- [ ] **Verify lesson prose accuracy** — the 4 NEW lessons describe APIs; spot-check that descriptions match actual behavior (e.g., entity extraction lesson says "three-stage pipeline" — does the package actually run spaCy → GLiNER → LLM in sequence?)
- [ ] **Verify tag boundaries** — ensure tagged sections in solutions produce sensible standalone code snippets when extracted by AsciiDoctor

---

## Open Questions (added 2026-03-02)

### 1. `run_all.sh` missing files 8–11 — RESOLVED

**File:** `run_all.sh`
**Problem:** The script only runs the original 7 solutions. The 4 new files (hybrid_provider, entity_extraction, reasoning_memory, gds_integration) are not included.
**Resolution:** Update `run_all.sh` to include all 11 files. Add the 4 new entries to the `scripts` array.

### 2. Test assertions for files 8–11 need different output patterns — RESOLVED

**Problem:** The existing 7 tests all assert on `"User:"` and `"Answer:"` (or similar agent output patterns). But the new files have different output.

**Resolution:** Follow the `genai-integration-langchain` reference repo pattern, which uses two assertion styles:
- **Structured output** (`output.startswith("Answer:")` or `"User:" in output`) — for agent-based solutions
- **Non-empty check** (`assert output > ""`) — for solutions with variable/non-agent output

Apply as follows:
| File | Assertion Pattern |
|------|-------------------|
| `hybrid_provider.py` | `assert "User:" in output` and `assert "Answer:" in output` (matches existing pattern) |
| `entity_extraction.py` | `assert "Added entity:" in output` |
| `reasoning_memory.py` | `assert "Recorded trace:" in output` or `assert output > ""` |
| `gds_integration.py` | `assert "User:" in output` and `assert "Answer:" in output` (matches existing pattern) |

### 3. `reasoning_memory.py` — `streaming_example()` is defined but never called — RESOLVED

**File:** `genai-maf-context-providers/solutions/reasoning_memory.py` lines 50–71
**Problem:** The `streaming_example()` function is defined and tagged (`# tag::streaming_recorder[]`) for lesson extraction, but `main()` never calls it.

**Resolution:** This is **intentional and correct**. The lesson (module 4, lesson 5 "Reasoning Memory") includes the `streaming_recorder` tag as a standalone code snippet to show the API. The tagged blocks in the solution file exist for AsciiDoc `include::` extraction — they don't all need to be called in `main()`. This is the same pattern used in `entity_extraction.py` (see #4). **No fix needed.**

### 4. `entity_extraction.py` — `settings_with_merge` and `settings_with_resolution` are unused — RESOLVED

**File:** `genai-maf-context-providers/solutions/entity_extraction.py` lines 31–59
**Problem:** Three `MemorySettings` objects defined but only one used at runtime.

**Resolution:** Same as #3 — **intentional and correct**. The lesson (module 4, lesson 2 "Entity Extraction Pipeline") includes all three tagged blocks as separate code examples:
- `tag=settings` — shown under "Configuring Extraction"
- `tag=merge_strategy` — shown under "Merge Strategies"
- `tag=resolution` — shown under "Entity Deduplication"
- `tag=manual_entity` — shown under "Automatic vs Manual Extraction"

Each tagged block is a self-contained code snippet for the lesson. Only `manual_entity` runs in `main()` because the other settings are configuration examples, not executable demos. **No fix needed.**

### 5. `gds_integration.py` — `create_gds_tools()` is unnecessarily async — RESOLVED

**File:** `genai-maf-context-providers/solutions/gds_integration.py` lines 46–49
**Problem:** `create_gds_tools(memory)` is declared `async def` but the inner call is not awaited.

**Resolution:** Verified that `create_memory_tools()` is **synchronous** (signature: `def create_memory_tools(memory, include_gds_tools=True) -> list[FunctionTool]`). The `async` wrapper is a no-op. **Fix:** Remove `async` from the wrapper to follow best practices, since the function contains no awaitable calls.

### 6. entity_extraction lesson confidence claim — RESOLVED

**Problem:** EXERCISES.md bug #1 noted the lesson says "Each entity node stores the ... confidence score" and questioned whether this was accurate given the `add_entity()` bug.

**Resolution:** The lesson prose is **accurate**. The confidence score on entity nodes comes from the *extraction pipeline* (spaCy/GLiNER assign confidence scores during extraction). The bug is only in the `add_manual_entity()` code example where `confidence=0.95` is passed as a direct parameter to `add_entity()` — that parameter doesn't exist on the API. The lesson text about entity nodes storing confidence is correct because the pipeline stores it, not the `add_entity()` call. **Lesson prose: no fix needed. Solution code: fix as documented in Bugs to Fix #1.**
---

## Test Plan

### Phase 1: Fix Known Bugs (no sandbox needed) — COMPLETE Mar 2

1. ~~Fix `confidence=0.95` bug in `entity_extraction.py` solution~~ — DONE
2. ~~Fix `async` wrappers in `gds_integration.py` solution~~ — DONE
3. ~~Update corresponding skeleton if needed~~ — Not needed (skeleton has TODOs only)
4. ~~Verify lesson.adoc accuracy for the confidence claim~~ — Lesson prose is correct
5. ~~Add lesson-only comments to tagged blocks~~ — DONE

### Phase 2: Static Verification (no sandbox needed) — COMPLETE Mar 2

1. ~~AST syntax check all 12 files (11 solutions + test file)~~ — All pass
2. ~~AST syntax check all 4 skeleton files~~ — All pass
3. ~~Verify all imports resolve against installed packages~~ — All 13 imports resolve
4. ~~Verify API signatures match solution code~~ — All verified (sync/async, params)
5. ~~Verify installed package versions satisfy requirements.txt~~ — All 12 packages OK
6. ~~Verify pytest discovers all 11 tests~~ — `pytest --collect-only` shows 11 items
7. ~~Python version~~ — 3.12.12 (matches devcontainer spec of 3.12)

### Phase 3: Live Testing (requires Neo4j sandbox + OpenAI key)

1. Provision a fresh recommendations sandbox
2. Run `setup.py` to load embeddings and create indexes
3. Run `test_environment.py` to verify connections
4. Run original 7 solutions (confirm still working):
   ```bash
   cd genai-maf-context-providers
   python solutions/simple_agent.py
   python solutions/simple_context_provider.py
   python solutions/fulltext_context_provider.py
   python solutions/vector_context_provider.py
   python solutions/graph_enriched_provider.py
   python solutions/memory_context_provider.py
   python solutions/memory_tools_agent.py
   ```
5. Run 4 NEW solutions:
   ```bash
   python solutions/hybrid_provider.py
   python solutions/entity_extraction.py
   python solutions/reasoning_memory.py
   python solutions/gds_integration.py
   ```
6. Run full test suite:
   ```bash
   cd ..
   pytest genai-maf-context-providers/solutions/test_solutions.py -v
   ```

### Phase 4: End-to-End Course Verification

1. Run course QA tests:
   ```bash
   cd /Users/ryanknight/projects/graphacademy/courses
   COURSES=genai-maf-context-providers npm run test:qa
   ```
2. Start local dev and verify `include::` directives resolve (requires companion repo pushed to GitHub)
