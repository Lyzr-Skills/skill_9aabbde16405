---
name: northwind-restocking-fee
description: Compute the exact restocking fee and final refund for a Northwind product return, given the item price and its condition (unopened, opened, or defective). Use whenever a customer asks how much they will be refunded on a return, or what the restocking fee will be.
---

# Northwind Restocking Fee Calculator

This skill computes the restocking fee and final refund for a return using Northwind's
policy. It **runs real code**, so the numbers are exact, not estimated.

## Policy
- **unopened** — full refund, no restocking fee.
- **opened** (non-defective) — 10% restocking fee.
- **defective** — full refund, no restocking fee.

## How to use
When a customer asks about a refund or restocking fee on a return, determine the item
**price** and **condition** (unopened / opened / defective), then run the bundled script
to compute the exact amounts:

```bash
python scripts/restocking_fee.py --price <PRICE> --condition <unopened|opened|defective>
```

The script prints JSON containing `restocking_fee` and `refund`. Report those exact
figures to the customer. Do not estimate the amounts yourself; always run the script so
the number is computed, not guessed.
