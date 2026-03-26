#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "fixtures" / "csvgroupby" / "orders-120000.csv"
ROWS = 120_000
CUSTOMERS = 1_000
SKUS = 400
MODULUS = 2_147_483_647
MULTIPLIER = 48_271


def next_state(state: int) -> int:
    return (state * MULTIPLIER) % MODULUS


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    state = 1
    with OUTPUT.open("w", encoding="utf-8") as handle:
        handle.write("customer_id,sku,qty,cents\n")
        for _ in range(ROWS):
            state = next_state(state)
            customer = f"cust{state % CUSTOMERS:04d}"
            state = next_state(state)
            sku = f"sku{state % SKUS:03d}"
            state = next_state(state)
            qty = 1 + state % 7
            state = next_state(state)
            cents = 100 + state % 50000
            handle.write(f"{customer},{sku},{qty},{cents}\n")


if __name__ == "__main__":
    main()
