import math
import numpy
import scipy
import csv
import urllib
import datetime
import os

def pois(x, mean):
	result = ((mean ** x) * math.exp(- mean))/math.factorial(x)
	return result

def bivpois(x, y, lambda1, lambda2, lambda3):
	if x == 0 or y == 0:
		probabilityMatrix = [ [ 0 for i in range(x+1) ] for j in range(y+1) ]
		probabilityMatrix[x][y] = math.exp( - lambda3) * pois(x, lambda1) * pois(y, lambda2)
	else:
		probabilityMatrix = [ [ 0 for i in range(x+1) ] for j in range(y+1) ]
		probabilityMatrix[0][0] = math.exp(-lambda1 - lambda2 - lambda3)
		for i in range(1, x+1):
			probabilityMatrix[i][0] = (probabilityMatrix[i-1][0] * lambda1)/(i)
		for j in range(1, y+1):
			probabilityMatrix[0][j] = (probabilityMatrix[0][j-1] * lambda2)/(j)
		for j in range(1, y+1):
			for i in range(1,x+1):
				probabilityMatrix[i][j] = (lambda1 * probabilityMatrix[i-1][j] + lambda3 * probabilityMatrix[i-1][j-1])/(i)
	return probabilityMatrix

def covariance(homeGoals, awayGoals):
	averageHomeGoals = sum(homeGoals)/len(homeGoals) 
	averageAwayGoals = sum(awayGoals)/len(awayGoals) 
	covariance = 0
	for i in range(len(homeGoals)):
		covariance += (homeGoals[i] - averageHomeGoals)*(awayGoals[i] - averageAwayGoals)
	covariance = covariance/(len(homeGoals)-1)
	return covariance




print(nilNil, numberOfDraws, count, nilNil/count, numberOfDraws/count)
