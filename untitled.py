import math
import numpy
import scipy
import csv
import urllib
import datetime
import os
	
def nilNilProb(homeTeam, awayTeam):
	with open('E0.csv') as csvfile:
		count1 = 0
		count2 = 0
		homeGames = {}
		awayGames = {}
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['HomeTeam'] == homeTeam or row['AwayTeam'] == homeTeam:
				print(row['HomeTeam'], row['AwayTeam'])
				count1 += 1
				if count1 > 8:
					break
		print(' ')	
		for row in reader:		
			if row['HomeTeam'] == awayTeam or row['AwayTeam'] == awayTeam:
				print(row['HomeTeam'], row['AwayTeam'])
				count2 +=1
				if count2 > 8:
					break
		

nilNilProb('Liverpool', 'Tottenham')