
import scipy
import cvxopt
import numpy
from cvxopt import matrix, solvers, blas
import pandas as pd 
from math import sqrt
import yahoo_api

import utils





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
        # print my_dict.keys()
        return_values= []
        for key in my_dict:
            
            value = my_dict[key]
            
            for i in range(len(value)-1):
                returns = float(value[i+1])/float(value[i])-1
                return_values.append(returns)
            new_dict[key] = return_values
           
    return_vec_array = numpy.array([new_dict.values()]) # creates an array of symbol returns, with symbols as rows and the returns as columns
    return_vec = return_vec_array.T # I need matrix for all dictionaries together
    return return_vec

# I expect returns to be multiple dictionaries here with key as symbol and values are the returns
# work on getting return_vec to sow in the right form of array and get it to the next function

#-------------------------------------------------------------




def optimal_portfolio(returns):

    # return_vec = historical_returns()

    n = len(returns)
    returns = numpy.asmatrix(returns)
    
    N = 100
    mus = [10**(5.0 * t/N - 1.0) for t in range(N)]
    # Convert to cvxopt matrices
    S = matrix(numpy.cov(returns))
    pbar = matrix(numpy.mean(returns, axis=1))
    
    # Create constraint matrices
    G = -matrix(numpy.eye(n))   # negative n x n identity matrix
    h = matrix(0.0, (n ,1))
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

    return numpy.asarray(wt), returns, risks



    # weights, returns, risks = optimal_portfolio(return_vec)


# optimal_portfolio([[-0.00355164, -0.00491801],[ 0.00681986,  0.0042362 ]])

if __name__ == "__main__":
    import algorithm_server
    