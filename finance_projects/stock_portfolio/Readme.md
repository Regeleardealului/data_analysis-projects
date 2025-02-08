# Diversified Portfolio Using Advanced Portfolio Optimization Techniques! 📈

I'm excited to share my latest project where I combined financial analysis, machine learning, and optimization techniques to create a diversified portfolio with risk-return characteristics. This project was created using Google Colab 🔨.

**Key Highlights:**
1. Stock Price Analysis 📊: I started by collecting historical stock price data for well-known companies like Apple, Microsoft, Google, Amazon, NVIDIA, Netflix, Cisco and Coca-Cola, spanning from 2010 to 2025, using data sourced from Yahoo Finance.
2. KMeans Clustering 💻: I used the KMeans clustering method to group stocks based on their annual returns and risk (variance). This approach allowed me to pick stocks that help reduce risk while aiming for higher returns.
3. Portfolio Optimization 💡: I ran Monte Carlo simulations to test thousands of different portfolio setups. I also used strategies like the Maximum Sharpe Ratio and Minimum Volatility to create portfolios that give the best returns for the level of risk involved.
4. Efficient Frontier 💹: I applied the concept of the Efficient Frontier, introduced by Harry Markowitz, to show the best risk-return combinations. This helps identify the portfolios that provide the highest return for the lowest possible risk.
5. Beta Calculations 📉: I calculated the beta of each stock to understand how much each stock moves in relation to the market (S&P 500). This helped me narrow down my stock choices to achieve better portfolio diversification.
   
## Conclusion:🧐
By applying these advanced optimization techniques, I've created a portfolio that offers an effective blend of risk and return, backed by statistical models.
- NVIDIA (NVDA) had the highest beta at 1.6573, indicating higher sensitivity to market fluctuations.
- Coca-Cola (KO) had the lowest beta at 0.5969, showing it's less volatile compared to the market.
- Maximum Sharpe Ratio Portfolio 💼: The portfolio with the highest Sharpe Ratio (a measure of risk-adjusted return) provides an annualized return of 34% with a 26% annualized volatility. The portfolio is mostly concentrated in Apple (AAPL),with the following allocations:
    1. AAPL: 33.07%
    2. AMZN: 7.28%
    3. NFLX: 19.32%
    4. NVDA: 27.02%
    5. KO: 13.31%
- Minimum Volatility Portfolio ⚖️: The portfolio with the minimum volatility (lowest risk) shows an annualized return of 14% and a 16% annualized volatility. This portfolio emphasizes Coca-Cola (KO), which has the largest allocation:
    1. KO: 70.49%
    2. CSCO: 8.96%
    3. AAPL: 5.74%

#PortfolioOptimization #DataScience #Finance #MachineLearning #InvestmentStrategies #RiskManagement #MonteCarloSimulation #KMeansClustering #SharpeRatio #EfficientFrontier #FinancialModeling #StockMarketAnalysis #Diversification