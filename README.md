# Bitcoin Trader Performance and Market Sentiment Analysis

## Project Overview

This project analyzes the relationship between trader performance on Hyperliquid and the Bitcoin Fear & Greed Index. The goal is to uncover patterns in profitability, win rates, and liquidation events across different market sentiment states.

## Datasets

- **Historical Trader Data**: Trade executions from Hyperliquid, including PnL, side, timestamps, etc.
- **Fear Greed Index**: Daily Bitcoin market sentiment data.

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Run the analysis:
   python src/analysis.py

3. View the report in reports/report.md

## Analysis

The analysis includes:
- Overall performance by sentiment
- Long vs Short performance
- Liquidation analysis
- Visualizations (if added)
