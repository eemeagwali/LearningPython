# portfolio_analysis_with_detailed_explanations.py
# Author: Subir's Python Class
# All key concepts in portfolio analysis explained with beginner-friendly examples

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# SECTION 1: UNDERSTANDING PORTFOLIO ANALYSIS
# =============================================================================

# A portfolio is a basket of assets, like stocks, that an investor holds.
# The goal of portfolio analysis is to assess returns, manage risk, and make informed decisions.

# =============================================================================
# SECTION 2: CREATING SAMPLE PRICE DATA
# =============================================================================

# Let's create sample prices for 3 stocks: Apple, Amazon, and Tesla over 4 days

data = {
   'AAPL': [105.05, 106.25, 104.75, 107.35],
   'AMZN': [310, 315, 312, 320],
   'TSLA': [250, 252, 248, 255]
}
dates = pd.date_range('2022-01-01', periods=4)
df = pd.DataFrame(data, index=dates)

# Calculate % change from previous day — gives daily returns
returns = df.pct_change()
print("\nDaily Returns:\n", returns)

# =============================================================================
# SECTION 3: PORTFOLIO RETURNS
# ============================================================================
# Let's say our portfolio has:
# - 0% in AAPL
# - 50% in AMZN
# - 25% in TSLA

weights = np.array([0, 0.5, 0.25])
# Calculate mean daily return of each stock
mean_daily_returns = returns.mean()

# Portfolio return is weighted average of individual returns
port_return = np.sum(mean_daily_returns*weights)
print("\nPortfolio Return (daily average):", port_return)

# =============================================================================
# SECTION 4: CUMULATIVE RETURN (Compounded Over Time)
# =============================================================================
# Add a 'Portfolio' column by multiplying weights
# Deep copy for independent manipulation
portfolio_returns = returns.copy(deep=True)
portfolio_returns['Portfolio'] = portfolio_returns.dot(weights)

# Compounding the return over time gives cumulative return
cumulative_returns = (1+portfolio_returns).cumprod()

# Plotting cumulative return
cumulative_returns['Portfolio'].plot(title='Portfolio Cumulative Return')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.grid(True)
plt.show()
