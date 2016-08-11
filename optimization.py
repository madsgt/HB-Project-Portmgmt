
import scipy
import cvxopt
import numpy
from cvxopt import matrix, solvers, blas
import pandas as pd 
from math import sqrt



from flask import Flask, render_template, redirect, flash, session, request
import jinja2


#query the db 