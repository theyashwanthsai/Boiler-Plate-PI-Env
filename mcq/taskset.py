"""mcq — the smallest possible verifiers v1 environment: single-turn multiple choice.

    TaskData   one question row plus its reference answer (`questions.jsonl`)
    Task       the reward: the letter inside <answer>...</answer> must equal the reference
    Taskset    loads the rows

    uv run vf-eval mcq --env.agent.harness.id null --env.agent.runtime.type subprocess -m <model> -n 5
"""

import json
import re
from pathlib import Path

import verifiers.v1 as vf

QUESTIONS = Path(__file__).parent / "questions.jsonl"

SYSTEM_PROMPT = """You answer multiple choice questions. Reply with the letter of the correct option, A, B, C or D,
inside answer tags and nothing else, e.g. <answer>B</answer>"""

ANSWER_TAG = re.compile(r"<answer>(.*?)</answer>", re.DOTALL)


def parse_letter(reply: str | None) -> str | None:
    """The single letter A-D inside the last <answer> tag, or None. Never raises."""
    tags = ANSWER_TAG.findall(reply or "")
    if not tags:
        return None
    letter = tags[-1].strip().upper()
    return letter if letter in {"A", "B", "C", "D"} else None   # "A or C", "AB", "" all fail


class MCQData(vf.TaskData):
    answer: str
    """The correct option letter. Never shown to the model."""


class MCQTask(vf.Task[MCQData]):
    @property
    def key(self) -> str:
        return self.data.id

    @vf.reward(weight=1.0)
    async def correct(self, trace: vf.Trace) -> float:
        return float(parse_letter(trace.last_reply) == self.data.answer)

    @vf.metric
    async def well_formed(self, trace: vf.Trace) -> float:
        return float(parse_letter(trace.last_reply) is not None)


class MCQTaskset(vf.Taskset[MCQTask, vf.TasksetConfig]):
    def load(self) -> list[MCQTask]:
        rows = [json.loads(line) for line in QUESTIONS.read_text().splitlines() if line.strip()]
        return [
            MCQTask(
                MCQData(
                    id=r["id"],
                    system_prompt=SYSTEM_PROMPT,
                    prompt=r["question"] + "\n\n" + "\n".join(f"{k}. {v}" for k, v in r["options"].items()),
                    answer=r["answer"],
                ),
                self.config.task,
            )
            for r in rows
        ]
