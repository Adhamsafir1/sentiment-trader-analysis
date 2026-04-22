# Bitcoin Market Sentiment Analysis

## Dataset Summary
- Historical Trades: 156955
- Sentiment Records: 2644
- Merged Records: 137395

## Performance by Sentiment
| classification   |   Total_Trades |   Winning_Trades |   Losing_Trades |   Avg_PnL |        Total_PnL |   Avg_Size_USD |   Win_Rate (%) |   Liquidation_Count |
|:-----------------|---------------:|-----------------:|----------------:|----------:|-----------------:|---------------:|---------------:|--------------------:|
| Fear             |          97055 |            40900 |            4797 |   55.6947 |      5.40544e+06 |        6012.69 |          42.14 |                   0 |
| Greed            |          26242 |            11053 |            1840 |   81.6813 |      2.14348e+06 |        3145.47 |          42.12 |                   0 |
| Neutral          |           7136 |             2265 |             545 |   22.2454 | 158743           |        3056.74 |          31.74 |                   0 |
| Extreme Greed    |           6962 |             3412 |             920 |   25.4188 | 176965           |        5660.27 |          49.01 |                   0 |

## Long vs Short Performance
| classification   | Trade_Type   |   Total_Trades |   Win_Rate |   Avg_PnL |
|:-----------------|:-------------|---------------:|-----------:|----------:|
| Extreme Greed    | Long         |             88 |       0    |   0       |
| Extreme Greed    | Short        |             75 |       0    |   0       |
| Fear             | Long         |           4691 |       0    |   0       |
| Fear             | Short        |           3908 |      77.46 |  52.3206  |
| Greed            | Long         |           2588 |       0    |   0       |
| Greed            | Short        |           4090 |      90.05 | 498.094   |
| Neutral          | Long         |            786 |       0    |   0       |
| Neutral          | Short        |            295 |      33.9  |   5.80018 |

