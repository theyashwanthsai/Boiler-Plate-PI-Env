# mcq

The smallest possible [verifiers](https://github.com/PrimeIntellect-ai/verifiers) v1 environment: single-turn
multiple choice, one exact reward. Use it as a template for new environments.

> Ported from verifiers 0.1.6 (`vf.SingleTurnEnv` + `vf.Rubric` + `vf.XMLParser`) to 0.4.0, where that API was removed.
> The v1 stack is `import verifiers.v1 as vf`, built from `TaskData`, `Task` and `Taskset`.

## Layout

    mcq/
    ├── mcq/
    │   ├── __init__.py        exports MCQTaskset (what `vf-eval mcq` loads)
    │   ├── taskset.py         MCQData (row + answer), MCQTask (@vf.reward), MCQTaskset (load)
    │   └── questions.jsonl    25 general-knowledge questions
    └── test_mcq.py            grader tests, no model needed

## v0 → v1, side by side

| 0.1.x (old) | 0.4.0 (v1) |
|---|---|
| `load_environment()` returns `vf.SingleTurnEnv(dataset=…)` | the package exports a `vf.Taskset` subclass with `load()` |
| a HF `Dataset` with `question` / `answer` columns | a list of `Task(TaskData(prompt=…, answer=…))` |
| `vf.Rubric(funcs=[…], weights=[…])` | `@vf.reward(weight=…)` methods on the `Task` |
| `vf.XMLParser(["answer"])` | parse `trace.last_reply` yourself (`parse_letter`) |
| the env runs the model loop | a **harness** runs the model (`null` = plain chat; `bash`, `codex`, `claude_code`, …) |
| `env.evaluate_sync(client, model)` | `vf-eval mcq -m <model>`; traces land in `outputs/` |

## Run

    uv sync
    uv run pytest -q                                   # grader tests

    # any OpenAI-compatible endpoint; here a local Ollama model
    OLLAMA_KEY=ollama uv run vf-eval mcq -m qwen3-coder:30b \
        --client.base-url http://localhost:11434/v1 --client.api-key-var OLLAMA_KEY \
        --env.agent.harness.id null --env.agent.runtime.type subprocess --no-push -n 25

`--env.agent.runtime.type subprocess` runs locally; the default is a Prime sandbox (needs `PRIME_API_KEY`).
`--no-push` keeps results local. Traces go to `outputs/mcq--<model>--null--<id>/traces.jsonl`.

## Why this is only a template

A model that always answers "B" scores 44% here (11 of 25 answers are B, none are A), and the questions are trivia
every model knows. It shows the plumbing, not a useful signal. A real environment needs a verifier that cannot
be guessed and tasks that a lazy policy fails: see `turilabs-envs/00-tictactoe` for one built that way.
