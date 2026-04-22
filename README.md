# Bitcoin Trader Performance and Market Sentiment Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![GitHub repo size](https://img.shields.io/github/repo-size/Adhamsafir1/sentiment-trader-analysis)](https://github.com/Adhamsafir1/sentiment-trader-analysis)

## 📊 Project Overview

This project analyzes the relationship between trader performance on Hyperliquid (a decentralized exchange) and the Bitcoin Fear & Greed Index. By merging historical trade data with market sentiment indicators, we uncover patterns in profitability, win rates, liquidation events, and directional bias across different sentiment states (Fear, Greed, Neutral, Extreme Greed).

**Key Insights:**
- Traders perform best during **Greed** periods with a 42.12% win rate.
- Short positions dominate profitable trades, especially in Greed sentiment.
- No liquidations observed in the dataset, indicating stable market conditions during the analyzed period.

## 🗂️ Table of Contents

- [Features](#-features)
- [Datasets](#-datasets)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Analysis Results](#-analysis-results)
- [Visualizations](#-visualizations)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## ✨ Features

- **Data Merging & Preprocessing**: Combines trade data with sentiment indices.
- **Performance Metrics**: Calculates win rates, PnL, and trade counts by sentiment.
- **Directional Analysis**: Compares Long vs. Short performance.
- **Liquidation Tracking**: Identifies high-risk periods.
- **Automated Reporting**: Generates Markdown reports and visualizations.
- **Modular Code**: Easy to extend for additional analyses.

## 📁 Datasets

- **Historical Trader Data** (`data/historical_data.csv`): Trade executions from Hyperliquid, including PnL, trade direction, timestamps, and sizes.
- **Fear & Greed Index** (`data/fear_greed_index.csv`): Daily Bitcoin market sentiment scores (0-100) categorized as Fear, Greed, etc.

*Note: Datasets are included in the repository for reproducibility.*

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Adhamsafir1/sentiment-trader-analysis.git
   cd sentiment-trader-analysis
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the analysis**:
   ```bash
   python src/analysis.py
   ```

## 🚀 Usage

1. Place your data files in the `data/` directory.
2. Execute the script to generate reports and visualizations.
3. View results in `reports/report.md` and PNG files in `reports/`.

### Example Output
- **Report**: Detailed Markdown summary with tables and insights.
- **Plots**: Win rate by sentiment, average PnL, and long/short comparisons.

## 📂 Project Structure

```
sentiment-trader-analysis/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── data/                     # Input datasets
│   ├── fear_greed_index.csv
│   └── historical_data.csv
├── src/                      # Source code
│   └── analysis.py           # Main analysis script
├── outputs/                  # Generated outputs (plots, cleaned data)
├── reports/                  # Final reports and visualizations
│   ├── report.md
│   ├── statistics.txt
│   └── *.png                 # Charts
└── .gitignore                # Files to ignore in Git
```

## 📈 Analysis Results

Based on the latest run (137,395 merged trades):

### Performance by Sentiment
| Sentiment      | Total Trades | Win Rate (%) | Avg PnL (USD) | Best For |
|----------------|--------------|--------------|---------------|----------|
| Fear          | 97,055      | 42.14       | 55.69        | Balanced |
| Greed         | 26,242      | 42.12       | 81.68        | High PnL |
| Neutral       | 7,136       | 31.74       | 22.25        | Low Risk |
| Extreme Greed | 6,962       | 49.01       | 25.42        | High Win Rate |

### Key Findings
- **Highest Win Rate**: Extreme Greed (49.01%)
- **Best PnL**: Greed periods (81.68 USD avg)
- **Directional Bias**: Shorts outperform longs, especially in Greed (90.05% win rate)
- **Liquidations**: None observed across sentiments

For full details, see [`reports/report.md`](reports/report.md).

## 📊 Visualizations

Generated plots include:
- Win Rate by Sentiment
- Average PnL by Sentiment
- Long vs Short Win Rate

*View examples in `reports/` directory.*

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request.

### Guidelines
- Ensure code is well-documented.
- Add tests for new features.
- Update README if needed.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Author**: Adham Safir
- **GitHub**: [Adhamsafir1](https://github.com/Adhamsafir1)
- **Email**: [your-email@example.com] (replace with actual)

---

*Built with ❤️ for data-driven trading insights.*
