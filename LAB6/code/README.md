# Food Delivery – Lab 6: Code and Branch Coverage

## Overview

This folder contains the Food Delivery application and the two test suites required for Lab 6.

The application (`food_delivery.py`) provides three functions:

- `delivery_charge(distance_km, order_value, is_raining)`: calculates the delivery charge based on distance, order value, and rain.
- `apply_coupon(order_value, code, is_first_order)`: applies a valid coupon when its conditions are satisfied.
- `estimated_time(distance_km, is_peak_hour, restaurant_busy)`: estimates delivery time based on distance, peak hours, and restaurant workload.

## Files

| File | Description |
|---|---|
| `food_delivery.py` | Application module being tested. |
| `CodeCoverageTest_food_delivery.py` | Test cases used for line/code coverage analysis. |
| `BranchCoverageTest_food_delivery.py` | Test cases used for branch coverage analysis. |

## Requirements

- Python 3.x
- pytest
- coverage

Install the required packages:

```bash
python -m pip install pytest coverage
```

## Run Code Coverage

Run the code-coverage test suite:

```bash
coverage erase
coverage run --source=food_delivery -m pytest -v CodeCoverageTest_food_delivery.py
coverage report -m
```

The target is at least 90% code coverage.

## Run Branch Coverage

Run the branch-coverage test suite:

```bash
coverage erase
coverage run --branch --source=food_delivery -m pytest -v BranchCoverageTest_food_delivery.py
coverage report -m
```

The target is at least 90% branch coverage.

## Understanding the Reports

- **Stmts**: number of executable statements measured.
- **Miss**: number of statements not executed by the tests.
- **Branch**: number of measured branch possibilities.
- **BrPart**: number of branches that were only partially covered.
- **Cover**: overall coverage percentage reported by coverage.py.

Use the terminal output from your own test execution as the evidence for the submission. Capture separate screenshots for code coverage and branch coverage after the tests have completed.

## Notes

- Run the commands from this directory, where `food_delivery.py` and the test files are located.
- The application source is kept separate from the test suites.
- Keep the code-coverage and branch-coverage test files separate, as required by the lab deliverables.
