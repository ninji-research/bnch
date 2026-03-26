#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "fixtures" / "joinagg" / "users-events-180000.txt"
USERS = 40_000
EVENTS = 180_000
MODULUS = 2_147_483_647
MULTIPLIER = 48_271
REGIONS = ("north", "south", "east", "west", "central", "coastal", "metro", "rural")
TIERS = ("free", "plus", "team", "enterprise")
KINDS = ("view", "click", "sync", "upload", "noop")


def next_state(state: int) -> int:
    return (state * MULTIPLIER) % MODULUS


def user_id(index: int) -> str:
    return f"user{index:05d}"


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    state = 1
    with OUTPUT.open("w", encoding="utf-8") as handle:
        handle.write("[users]\n")
        handle.write("user_id,region,tier,status\n")
        for index in range(USERS):
            shuffled = (index * 1_531) % USERS
            state = next_state(state)
            region = REGIONS[state % len(REGIONS)]
            state = next_state(state)
            tier = TIERS[state % len(TIERS)]
            state = next_state(state)
            status = "active" if state % 5 != 0 else "inactive"
            handle.write(f"{user_id(shuffled)},{region},{tier},{status}\n")

        handle.write("[events]\n")
        handle.write("user_id,kind,latency_ms,bytes\n")
        for _ in range(EVENTS):
            state = next_state(state)
            user = state % (USERS + USERS // 8)
            state = next_state(state)
            kind = KINDS[state % len(KINDS)]
            state = next_state(state)
            latency_ms = 5 + state % 2000
            state = next_state(state)
            payload_bytes = 200 + state % 200_000
            handle.write(f"{user_id(user)},{kind},{latency_ms},{payload_bytes}\n")


if __name__ == "__main__":
    main()
