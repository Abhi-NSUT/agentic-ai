# Desk App: project workflow


## 1. What are we building?
A **support desk agent** for a small online shop. A customer types a question, and the agent picks the right **tool** to answer it:

| Question type | Example | Tool used |
|---|---|---|
| About *my* order | "Where is A17?" | `lookup_order` |
| Refund *my* order | "Refund A17" | `refund_order` |
| About shop rules | "Is shipping free?" | `search_policies` |

**The main security idea:** the customer's identity (`Customer.name`) is passed in by **our code** as *runtime context*. The model never sees it and can't change it. So the owner check lives **inside the tool**, not in the prompt, and a customer can't talk the model into showing someone else's order.

## 2. How the pieces fit
```
                 policies.py ──(chunks)──┐
                                         ▼
          word_embeddings.py ──► search.py ──► search_policies ─┐
                                                                 │
desk_tools.py: ORDERS, Customer, lookup_order, refund_order ────┤
                                                                 ▼
                         desk.py: create_agent(model, tools, context_schema=Customer)
                                                                 ▲
                         model = Groq gpt-oss-120b (real)   OR   DeskModel (scripted stand-in)
```

**One request, step by step:**
1. Our code calls `desk.invoke({"messages": [...]}, context=Customer("ravi"))`.
2. The model reads the question and the tool descriptions (docstrings), then decides which tool to call and with what `order_id` or `query`.
3. The tool runs. Order tools read `runtime.context.name` to check the owner.
4. The tool's text goes back to the model, which writes the final short reply.

## 3. Files (`src/desk_app/`)

| File | What it does | Status |
|---|---|---|
| `policies.py` | 3 policy docs (refunds, shipping, accounts) split into 5 chunks with `RecursiveCharacterTextSplitter` | ✅ |
| `word_embeddings.py` | `WordEmbeddings`: a toy embedder that hashes words into 256 buckets. Needs no API key. | ✅ |
| `search.py` | Puts the chunks in an `InMemoryVectorStore`. `search_policies` returns matches scoring ≥ 0.3, otherwise "No policy covers this." | ✅ |
| `desk_tools.py` | `ORDERS`, the `Customer` dataclass, and owner-checked `lookup_order` and `refund_order` | ✅ |
| `desk.py` | Builds the agent (`build_desk`, takes an optional stand-in model) and runs the three test questions | ✅ |
| `shop_model.py`, `desk_model.py` | Scripted fake model for exact, key-free tests | ✅ |
| `__init__.py` | `main()`, the entry point for `uv run desk-app`; calls `desk.run()` | ✅ |

## 4. What's done so far

| Step | What | Commit | How it was checked |
|---|---|---|---|
| 1 | `uv add langchain-text-splitters` | `8cb72a7` | install succeeded |
| 2 | `policies.py` | `8cb72a7` | 5 chunks created |
| 3 | `word_embeddings.py` makes `search.py` work | `8cb72a7` | "Is shipping free?" → shipping.md; "Do you sell bikes?" → "No policy covers this." |
| 4 | `desk_tools.py` | `e371767` | As Ravi: A17 is shown, C40 (Mei's) is refused, Z99 gets the same refusal, and the model sees only the `order_id` argument |
| 5 | `shop_model.py` + `desk_model.py` (`DeskModel` stand-in) | `22bb45c` | As Ravi, no API key: "Where is A17?" → shipped on 3 March; "Where are A17 and C40?" → both calls in one AI message, C40 refused; "Refund A17" → refunded; "Is shipping free?" → shipping.md; "Do you sell bikes?" → "No policy covers this." |
| 6 | `desk.py` on Groq `gpt-oss-120b`, run by `uv run desk-app` | _pending_ | As Ravi: A17 → "A17 shipped on 3 March."; "Is shipping free?" → free over 50 euros; C40 → "C40 is not one of your orders." Exercises: Z99 → same refusal; without `search_policies` → "I don't have that information"; message list = human → ai(tool call) → tool → ai |

Pushed to `origin/main` on GitHub.

## 5. What's next

**Next lessons**
- 38 · Desk guardrails: rules, plus a stop for approval before `refund_order` runs.
- 39 · A morning at the desk: running many customers' questions.
- 40 · Desk threads: memory across turns.
- 41 · Desk tests: exact tests using `DeskModel`, with no API key.

## 6. Commands
```sh
cd desk-app
uv run desk-app                      # run the desk on Groq
uv add <package>                     # add a dependency
uv run python -c "from desk_app.search import search_policies; print(search_policies.invoke({'query': 'Is shipping free?'}))"
```
If your editor can't resolve imports, select the interpreter `desk-app/.venv/bin/python`.
