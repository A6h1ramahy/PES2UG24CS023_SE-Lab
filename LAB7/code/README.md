# LAB 7 – Fuzz Testing

## Assignment

Food Delivery Application – Fuzz Testing using Hypothesis.

## Overview

This assignment explores property-based fuzz testing using
the Python Hypothesis library.

The original application contained three functions:

1. parse_order()
2. delivery_eta()
3. coupon_discount()

These functions were tested with automatically generated
inputs to identify unexpected behaviour and input validation bugs.

## Technologies Used

- Python
- Hypothesis
- Pytest

## Installation

Install the dependencies:

```bash
python -m pip install -r requirements.txt