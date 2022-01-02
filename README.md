# MonteCarlo_Portfolio
Calculation of risk in a cryptocurrency portfolio by the [Monte Carlo method](https://www.investopedia.com/articles/investing/112514/monte-carlo-simulation-basics.asp)

![Image text](https://github.com/jblanco89/MonteCarlo_Portfolio/blob/main/output_plot_montecarlo.png)

The image above shows the output simulation after trying 90.000 random values by using the Monte-Carlo Method. 

In this case, I have calculated the Sharpe ratio and also compared it with the minimum volatility output. After getting the best results, I wanted to try a random portofolio configuration in order to determine the Sharpe ratio location in the simulation plot. 

The red cross represents the Max Sharpe Ratio.

The green cross represents the Minimum Volatility Ratio.

The black cross represents the Sharpe Ratio of the Real Portfolio 

In this case, I've tried only with cryptocurrencies such as: `LTC`, `SOL`, `CAKE`, `ADA` and `RAY`

Price's data was taken using the official `Python client` of `Coingecko API` available [Here](https://github.com/man-c/pycoingecko)

