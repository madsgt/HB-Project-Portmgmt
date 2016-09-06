Welcome to your Stock Pie!

Stock Pie is your guide to allocating you money to the stocks of your choice. It takes your choices and finds the most optimum portfolio allocation for the set of stocks. This means you are assured of good risk adjusted returns, more value for the buck ! The built in algorithm ensures that the goal remains to optimally allocate your investments between different assets. Mean variance optimization (MVO) is a quantitative tool which will allow you to make this allocation by considering the trade-off between risk and return. We have used Single period portfolio optimization using the mean and variance as formulated by Markowitz. Yahoo Finance API has been used to get the historical daily prices for past 3 years used to calculate the daily returns for the same period. Other inputs such as the expected return for each asset in the portfolio, the standard deviation of each asset (a measure of risk) and the correlation matrix between these assets was calculated using statistical methods from Python library.
The output is the efficient frontier, i.e. the set of portfolios with expected return greater than any other with the same or lesser risk, and lesser risk than any other with the same or greater return. THe output is simplified for the user by display of a donut chart that gives them the final percentage investment split for the 5 stocks they choose initially. The user now knows how to allocate his Investible surplus across the stocks he wants in his portfolio. 

 Tech Stack
 Stock Pie uses the following technologies/frameworks/libraries:

 PostgreSQL
 Python
 HTML, CSS
 JavaScript
 AJAX

 SQLAlchemy
 Flask
 Scipy, Numpy, CVXOPT, pandas, matplotlib
 Jinja
 Bootstrap
 JQuery
 Chart.js
 AJAX
 
 API Used:
 Yahoo Finance 