#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "fixtures" / "sortuniq" / "words-250000.txt"
COUNT = 250_000

PREFIXES = (
    "al", "bar", "cor", "den", "el", "far", "gan", "hal", "in", "jor",
    "kal", "lor", "mor", "nar", "or", "pra", "quin", "ran", "sol", "tor",
    "ul", "vor", "wen", "xer", "yor", "zen",
)
MIDDLES = (
    "a", "e", "i", "o", "u", "ar", "en", "il", "or", "un", "ast", "end",
    "ing", "orn", "uth", "ell",
)
SUFFIXES = (
    "a", "ac", "al", "an", "ar", "e", "el", "en", "er", "ess", "ic", "id",
    "il", "in", "ion", "is", "on", "or", "os", "um", "us", "y",
)


def lcg(seed: int) -> int:
    return (seed * 1_664_525 + 1_013_904_223) & 0xFFFFFFFF


def make_word(state: int) -> tuple[str, int]:
    state = lcg(state)
    prefix = PREFIXES[state % len(PREFIXES)]
    state = lcg(state)
    middle = MIDDLES[state % len(MIDDLES)]
    state = lcg(state)
    suffix = SUFFIXES[state % len(SUFFIXES)]
    state = lcg(state)
    if state & 3 == 0:
        word = prefix + suffix
    else:
        word = prefix + middle + suffix
    return word, state


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    state = 1
    lines: list[str] = []
    for index in range(COUNT):
        word, state = make_word(state)
        if state & 15 == 0:
            word, state = make_word(state)
        lines.append(word)
        if index % 97 == 0:
            lines.append("")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
