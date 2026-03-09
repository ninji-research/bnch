#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "fixtures" / "knucleotide" / "knucleotide-250000.fasta"

IM = 139968
IA = 3877
IC = 29573
LINE_LENGTH = 60
SEED = 42
LENGTH = 250_000

HOMO_SAPIENS = (
    ("a", 0.3029549426680),
    ("c", 0.1979883004921),
    ("g", 0.1975473066391),
    ("t", 0.3015094502008),
)


def cumulative_table() -> list[tuple[float, str]]:
    total = 0.0
    table: list[tuple[float, str]] = []
    for char, probability in HOMO_SAPIENS:
        total += probability
        table.append((total, char))
    return table


def next_random(seed: int) -> tuple[int, float]:
    seed = (seed * IA + IC) % IM
    return seed, seed / IM


def build_sequence(length: int) -> str:
    table = cumulative_table()
    seed = SEED
    chars: list[str] = []
    for _ in range(length):
        seed, value = next_random(seed)
        for threshold, char in table:
            if value < threshold:
                chars.append(char)
                break
    return "".join(chars)


def main() -> int:
    sequence = build_sequence(LENGTH)
    FIXTURE.parent.mkdir(parents=True, exist_ok=True)
    with FIXTURE.open("w", encoding="utf-8") as handle:
        handle.write(">THREE Homo sapiens frequency\n")
        for start in range(0, len(sequence), LINE_LENGTH):
            handle.write(sequence[start : start + LINE_LENGTH])
            handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
