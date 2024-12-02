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
    python main.py
    ```