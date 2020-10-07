# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 2017

@author: Giuseppe Armenise
"""
from __future__ import division, print_function

import sys

import numpy as np


# function that generates a sequence of inputs GBN
# length_arg: number of wished inputs
# prob_switch: probability of switching (no switch: 0<x<1 :always switch)
# Range: range of the inputs, example: Range=[3.,15.]
def GBN_seq(length_arg, prob_switch, Range=[-1.0, 1.0]):
    min_Range = min(Range)
    max_Range = max(Range)
    gbn = np.ones(length_arg)
    for i in range(length_arg - 1):
        prob = np.random.random()
        gbn[i + 1] = gbn[i]
        if prob < prob_switch:
            gbn[i + 1] = -gbn[i + 1]
    for i in range(length_arg):
        if gbn[i] > 0.:
            gbn[i] = max_Range
        else:
            gbn[i] = min_Range
    return gbn

# function which generates a sequence of inputs as Random walk
# length_arg: time length of desidered input
# sigma: standard deviation (mobility) of randow walk
# rw0: initial value    
def RW_seq(length_arg,rw0, sigma = 1):
    rw = rw0*np.ones(length_arg)
    for i in range (length_arg-1):
        # return random sample from a normal (Gaussian) distribution with:
        # mean = 0.0, standard deviation = sigma, and length = 1
        delta = np.random.normal(0., sigma, 1)
        # refresh input
        rw[i+1] = rw[i] + delta
    return rw 


# this function adds a white noise to a signal
# y:clean signal
# A_rel: relative amplitude (0<x<1) to the standard deviation of y (example: 0.05)
# noise amplitude=  A_rel*(standard deviation of y)
def white_noise(y, A_rel):
    num = y.size
    errors = np.zeros(num)
    y_err = np.zeros(num)
    Ystd = np.std(y)
    scale = np.abs(A_rel * Ystd)
    if scale < np.finfo(np.float32).eps:
        scale = np.finfo(np.float32).eps
        sys.stdout.write("\033[0;35m")
        print("Warning: A_rel may be too small, its value set to the lowest default one");
        sys.stdout.write(" ")
    errors = np.random.normal(0., scale, num)
    y_err = y + errors
    return errors, y_err


# this function generates a white noise matrix (rows with zero mean), L:size (columns), Var: variance vector
# e.g.   noise=white_noise_var(100,[1,1]) , noise matrix has two row vectors with variance=1
def white_noise_var(L, Var):
    Var = np.array(Var)
    n = Var.size
    noise = np.zeros((n, L))
    for i in range(n):
        if Var[i] < np.finfo(np.float32).eps:
            Var[i] = np.finfo(np.float32).eps
            sys.stdout.write("\033[0;35m")
            print("Warning: Var[", i,
                  "] may be too small, its value set to the lowest default one");
            sys.stdout.write(" ")
        noise[i, :] = np.random.normal(0., Var[i] ** 0.5, L)
    return noise


# rescaling an array to its standard deviation. It gives the array rescaled: y=y/(standard deviation of y)
# and thestandard deviation: ex [Ystd,Y]=rescale(Y)
def rescale(y):
    ystd = np.std(y)
    y_scaled = y/ystd
    return ystd, y_scaled


def information_criterion(K, N, Variance, method='AIC'):
    if method == 'AIC':
        IC = N * np.log(Variance) + 2 * K
    elif method == 'AICc':
        if N - K - 1 > 0:
            IC = N * np.log(Variance) + 2 * K + 2 * K * (K + 1) / (N - K - 1)
        else:
            IC = np.inf
            sys.exit('Number of data is less than the number of parameters, AICc cannot be applied')
    elif method == 'BIC':
        IC = N * np.log(Variance) + K * np.log(N)
    return IC


def mean_square_error(predictions, targets):
    return ((predictions - targets) ** 2).mean()
