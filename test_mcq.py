"""Grader tests: no model needed. Run with `uv run pytest -q`."""

import verifiers.v1 as vf

from mcq.taskset import MCQTaskset, parse_letter


def test_parse_accepts_one_letter():
    assert parse_letter("<answer>C</answer>") == "C"
    assert parse_letter("thinking... <answer> b </answer>") == "B"
    assert parse_letter("<answer>A</answer> wait, <answer>D</answer>") == "D"   # last tag wins


def test_parse_rejects_hedging_and_junk():
    for reply in ["C", "<answer>A or C</answer>", "<answer>AB</answer>", "<answer></answer>",
                  "<answer>E</answer>", "", None, "<answer>C"]:
        assert parse_letter(reply) is None, reply


def test_pack_loads_and_answers_are_letters():
    tasks = MCQTaskset(vf.TasksetConfig()).load()
    assert len(tasks) == 25
    assert len({t.key for t in tasks}) == 25
    assert all(t.data.answer in "ABCD" for t in tasks)


def test_always_same_letter_scores_like_chance():
    # a lazy policy that always answers the same letter must not beat ~chance by much
    tasks = MCQTaskset(vf.TasksetConfig()).load()
    for letter in "ABCD":
        share = sum(t.data.answer == letter for t in tasks) / len(tasks)
        assert share <= 0.5, (letter, share)
