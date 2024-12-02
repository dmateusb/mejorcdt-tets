# Profitability Calculator

## Overview

The `ProfitabilityCalculator` is a Python script designed to process financial data from a CSV file and calculate various financial metrics such as late payment interest and return on investment (ROI).

## Features

- Load financial data from a CSV file.
- Calculate late payment interest based on an annual anticipated rate.
- Calculate return on investment (ROI) for a given amount and period.
- Filter rates based on period and amount.

## Requirements

- Python 3.6 or higher
- pandas library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/profitability_calculator.git
    cd profitability_calculator
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Prepare your CSV file with the following columns:
    - `consecutivo`
    - `fecha`
    - `minmonto` 
    - `maxmonto` 
    - `minplazo` 
    - `maxplazo` 
    - `tasa`
    - `banco`

2. Place your CSV file in the `data/raw/` directory.

3. Run the script:
    ```sh
    python profitability_calculator.py
    ```

## Example

Here is an example of how to use the `ProfitabilityCalculator` class in your script:

```python
    from profitability_calculator import ProfitabilityCalculator

    # Initialize the calculator
    calculator = ProfitabilityCalculator()

    # Calculate late payment interest
    annual_rate = 0.10  # 10% annual anticipated rate
    late_payment_interest = calculator.calculate_late_payment_interest(annual_rate)
    print(f"Late Payment Interest: {late_payment_interest:.4f}")

    # Calculate ROI
    amount = 1000  # Initial investment amount
    days = 30  # Investment period in days
    roi = calculator.calculate_roi(amount, days)
    print(f"ROI: {roi}")
```