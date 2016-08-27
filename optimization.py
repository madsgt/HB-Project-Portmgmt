
import scipy
import cvxopt
import numpy
from cvxopt import matrix, solvers, blas, printing
import pandas as pd
from math import sqrt
import yahoo_api
# import matplotlib.pyplot
import utils
import mpld3



from flask import Flask, render_template, redirect, flash, session, request
import jinja2

#-------------------------------------------------------------
def historical_returns(yahooapidata):
    """this function will calculate daily returns for the 3 yrs for a stock symbol """
    """the data input here are list of dictionaries that looks like below and for each symbol we 
    need to loop ,Calc-((adj close (t)/adj close(t-1)-1)/ for 3 years data  
    input data looks as below
    [{'GOOG': ['777.140015', '782.440002', '783.219971', '784.849976', '784.679993']},
    {'YHOO': ['42.490002', '42.669998', '42.939999', '41.27', '39.93', '39.240002']}] 

    output data will look like:
    [{'GOOG': ['4.5', '6.7', '1', '-2.14', '-3.5']},
    {'YHOO': ['-2.5', '2.4', '-1.88', '-3.5111', '3.9']}] 
    
    after that need to take keys of each dictionary as rows and the values as columns in matrix format
    """

    new_dict = {}
    for my_dict in yahooapidata:
        # print my_d+ct.keys()
        return_values= []
        for key in my_dict:
            
            value = my_dict[key]
            
            for i in range(len(value)-1):
                returns = float(value[i+1])/float(value[i])-1
                return_values.append(returns)
            new_dict[key] = return_values

    return new_dict.values(), new_dict.keys()
    """ The result is like ([[0.006819861154621076, 0.0009968419278234553, 0.0020811586276570093, -0.0002165802448849119], [-1.96, -1.7833333333333332, 0.8676063829787235, -2.1107630087436986]], ['GOOG', 'YHOO'])
    """

#-------------------------------------------------------------




def optimal_portfolio(returns):
   
   

    n = len(returns)
    returns = numpy.asmatrix(returns)
    
    N = 100
    mus = [10**(5.0 * t/N - 1.0) for t in range(N)]
    # Convert to cvxopt matrices
    S = matrix(numpy.cov(returns))
    pbar = matrix(numpy.mean(returns, axis=1))
    
    # Create constraint matrices
    m=[[-1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0],[0.0,-1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0],[0.0,0.0,-1.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0],[0.0,0.0,0.0,-1.0,0.0,0.0,0.0,0.0,1.0,0.0],[0.0,0.0,0.0,0.0,-1.0,0.0,0.0,0.0,0.0,1.0]]
    G = matrix(m)
  
    ab=[0,0,0,0,0,0.3,0.3,0.3,0.3,0.3]
    h=matrix(ab)

    # G = -matrix(numpy.eye(n))   # negative n x n identity matrix
    # h = matrix(0.0, (n ,1))
    A = matrix(1.0, (1, n))
    b = matrix(1.0)
    
    # Calculate efficient frontier weights using quadratic programming
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x'] 
                  for mu in mus]
    ## CALCULATE RISKS AND RETURNS FOR FRONTIER
    returns = [blas.dot(pbar, x) for x in portfolios]
    risks = [numpy.sqrt(blas.dot(x, S*x)) for x in portfolios]
    ## CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
    m1 = numpy.polyfit(returns, risks, 2)
    x1 = numpy.sqrt(m1[2] / m1[0])
    # CALCULATE THE OPTIMAL PORTFOLIO
    wt = solvers.qp(matrix(x1 * S), -pbar, G, h, A, b)['x']

    weights = matrix(wt)
    printing.options['dformat'] = '%.1f' #rounding up weights to 1 decimal

    # return numpy.asarray(wt)
    return weights  #changed in matrix
    """result looks like the follwg- 
    [0.1]
    [0.3]
    [0.3]
    [0.3]
    [0.0]"""

# to plot the efficient frontier in the front page 
# matplotlib.pyplot.plot(stds, means, 'o')
# matplotlib.pyplot.ylabel('mean')
# matplotlib.pyplot.xlabel('std')
# matplotlib.pyplot.plot(risks, returns, 'y-o')
  

    # return numpy.asarray(wt), returns, risks 

    # we have changed the matrix constraints for G and h to ensure no portfolio takes more than 30% of the allocation,currently works for 5 stovks

    # weights, returns, risks = optimal_portfolio(return_vec)



def final_portfolio(symbol_list):
    yahooapidata = yahoo_api.get_all_stock_data(symbol_list) # this gets api data for all the symbols
    historicalreturns = historical_returns(yahooapidata) # calcultes the returns for the symbols, output is a dictionary

   
    my_portfolio_values = optimal_portfolio(historicalreturns[0]) # take the returns as values and pass into the function
    my_tickers = historicalreturns[1] # the key is stored separately
    
    # new_valuelist = []
    # for value in my_portfolio_values:
    #     print value
    #     for i in value:
    #         print i
    #         new_value += value[i] 
    #     new_valuelist.append(new_value)
    #     print new_valuelist

    # return dict(zip(my_tickers, new_valuelist)) was trying to round 
        

   
 
    return dict(zip(my_tickers, my_portfolio_values)) 
    """ the results are {'GOOG': 0.09984881968219586, 'YHOO': 0.29996987179127077, 'AAPL': 0.2999752441661823, 'AA': 0.2999938062886864, 
    'MSFT': 0.00021225807166471572} """
  
  



 


if __name__ == "__main__":
    import algorithm_server
    print final_portfolio(["GOOG","YHOO","MSFT","AA","AAPL"])
    