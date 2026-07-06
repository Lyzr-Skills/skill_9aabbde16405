#!/usr/bin/env python3
"""Compute the restocking fee and refund for a Northwind return.

Northwind return policy (matches the Northwind Returns agent spec):
- unopened items ........ 30-day full refund, no restocking fee
- opened, non-defective . 15-day window, 10% restocking fee
- defective ............. 90-day free replacement or refund, no restocking fee

The point of this skill in the C3/C4 videos is that the agent RUNS this code to
get an exact number, instead of estimating it. Keep the output a clean, checkable
figure so "it computed, not guessed" is unmistakable on camera.

Usage:
    python restocking_fee.py --price 1299.00 --condition opened
    python restocking_fee.py '{"price": 1299.00, "condition": "opened"}'

Prints JSON: {condition, price, restocking_fee_rate, restocking_fee, refund}
Example: price 1299.00, condition opened -> fee 129.90, refund 1169.10
"""
import argparse
import json
import sys

# restocking-fee rate by item condition
RESTOCKING_RULES = {
    "unopened": 0.0,
    "opened": 0.10,      # opened, non-defective
    "defective": 0.0,
}


def compute(price, condition):
    condition = (condition or "").strip().lower()
    if condition not in RESTOCKING_RULES:
        raise ValueError(
            f"Unknown condition '{condition}'. "
            f"Use one of: {', '.join(RESTOCKING_RULES)}"
        )
    price = round(float(price), 2)
    rate = RESTOCKING_RULES[condition]
    fee = round(price * rate, 2)
    refund = round(price - fee, 2)
    return {
        "condition": condition,
        "price": price,
        "restocking_fee_rate": rate,
        "restocking_fee": fee,
        "refund": refund,
    }


def _parse_args():
    p = argparse.ArgumentParser(description="Northwind restocking-fee calculator")
    p.add_argument("payload", nargs="?", help='JSON string, e.g. {"price":1299,"condition":"opened"}')
    p.add_argument("--price", type=float)
    p.add_argument("--condition")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    if args.payload:
        data = json.loads(args.payload)
        price, condition = data.get("price"), data.get("condition")
    else:
        price, condition = args.price, args.condition
    if price is None or condition is None:
        print("error: provide price and condition", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(compute(price, condition), indent=2))
