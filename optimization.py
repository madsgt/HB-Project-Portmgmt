
import scipy
import cvxopt
import numpy
from cvxopt import matrix, solvers, blas
import pandas as pd 
from math import sqrt




from flask import Flask, render_template, redirect, flash, session, request
import jinja2

#-------------------------------------------------------------
#query the db for daily prices . DEFINE THIS
def get_allstocks_info(symbol):
    # """Takes in all stocks data by symbol and needs to give list of daily 'Close': '28.35' & mcap once(this is the last data pt)"""

    close_price = cccccc.query.filter_by(symbol=symbol).all() #what is the data type of this?

    #OR
    
    for symbol in symbols:
    # for each symbol
    or close_price = db.session.query(cccccc.id, cccccc.Close).all()
    & m_cap = db.session.query(cccccc.market_cap).one()
    print "%s, %s" % (symbol.close_price, symbol.m_cap)


pass

#-------------------------------------------------------------
# Fill in the following function or if function above works this may not be needed

def get_past_prices(data):  
    prices = data['']    
    return prices

pass






#-------------------------------------------------------------
def historical_returns(data):

pass

# function to calculate daily returns , (daily close (t)- daily close(t-1))/ for 3 years 


#-------------------------------------------------------------

def _ss(data, c=None):
    """Return sum of square deviations of sequence data.
    If ``c`` is None, the mean is calculated in one pass, and the deviations
    from the mean are calculated in a second pass. Otherwise, deviations are
    calculated from ``c`` as given. 
    """
    if c is None:
        c = mean(data)
    ss = _sum((x-c)**2 for x in data)
    # The following sum should mathematically equal zero, but due to rounding
    # error may not.
    ss -= _sum((x-c) for x in data)**2/len(data)
    assert not ss < 0, 'negative sum of square deviations: %f' % ss
    return ss

def variance(data, xbar=None):
	"""Return the sample variance of data.

	Statistics.py library info= data should be an iterable of Real-valued numbers, with at least two
	values. The optional argument xbar, if given, should be the mean of
    the data. If it is missing or None, the mean is automatically calculated.
    data is a sample from a population. 

    Examples:

    >>> data = [2.75, 1.75, 1.25, 0.25, 0.5, 1.25, 3.5]
    >>> variance(data)
    1.3720238095238095    """

    if iter(data) is data: #data is a collection object ,returns an iterator object
        data = list(data) #creates list of the data
	    n = len(data)
    if n < 2:
       raise StatisticsError('variance requires at least two data points')
    T, ss = _ss(data, xbar) #sum of squares of stddev
    return _convert(ss/(n-1), T)


def stdev(data, xbar=None):
    """Return the square root of the sample variance.
    See ``variance`` for arguments and other details.
    >>> stdev([1.5, 2.5, 2.5, 2.75, 3.25, 4.75])
    1.0810874155219827
    """
    var = variance(data, xbar)
    try:
        return var.sqrt()
    except AttributeError:
        return math.sqrt(var)

