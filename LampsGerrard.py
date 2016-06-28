import math
import numpy
import scipy
import csv
import urllib
import datetime
import os

def totalAverage(someList):
	answer = sum(som

with open('LampardGerrardOdds.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['HomeTeam'] == 'Chelsea':
			chelseaHomeOdds.append(float(row['B365H']))
		if row['AwayTeam'] == 'Chelsea':
			chelseaAwayOdds.append(float(row['B365A']))
		if row['HomeTeam'] == 'Liverpool':
			liverpoolHomeOdds.append(float(row['B365H']))
		if row['AwayTeam'] == 'Liverpool':
			liverpoolAwayOdds.append(float(row['B365A']))

print((totalAverage(liverpoolHomeOdds)+totalAverage(liverpoolAwayOdds))/2)
print((totalAverage(chelseaHomeOdds)+totalAverage(chelseaAwayOdds))/2)