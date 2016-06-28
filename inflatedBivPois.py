import math
import numpy
import scipy
import csv
import urllib
import datetime
import os

def average(someList):
	answer = sum(someList)/len(someList)
	return answer

def pois(x, mean):
	result = ((mean ** x) * math.exp(- mean))/math.factorial(x)
	return result

def bivpois(x, y, lambda1, lambda2, lambda3, nilNil):
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
	probabilityMatrix[0][0] = nilNil

	return probabilityMatrix

def covariance(homeGoals, awayGoals):
	averageHomeGoals = sum(homeGoals)/len(homeGoals) 
	averageAwayGoals = sum(awayGoals)/len(awayGoals) 
	covariance = 0
	for i in range(len(homeGoals)):
		covariance += (homeGoals[i] - averageHomeGoals)*(awayGoals[i] - averageAwayGoals)
	covariance = covariance/(len(homeGoals)-1)
	return covariance

def nilNilProb(homeTeam, awayTeam):
	with open('E0.csv') as csvfile:
		count = 0
		nilNil = 0
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['HomeTeam'] == homeTeam and row['AwayTeam'] == awayTeam:
				count+=1
				if row['FTHG'] == '0' and row['FTAG'] == '0':
					nilNil+=1
			if row['HomeTeam'] == awayTeam and row['AwayTeam'] == homeTeam:
				if row['FTHG'] == '0' and row['FTAG'] == '0':
					nilNil+=1
					count+=1		
	return nilNil/count

#download new data
def downloadData():
	from urllib import request
	response = request.urlopen("http://www.football-data.co.uk/mmz4281/1516/E0.csv")
	downloadValues = response.read()
	csvstr = str(downloadValues).strip("b'")
	lines = csvstr.split("\\r\\n")
	f = open("download.csv", "w")
	for line in lines:
	   f.write(line + "\n")
	f.close()
downloadData()

#update data
with open('download.csv') as csvfile:
	fieldnames = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A','BWH','BWD','BWA','IWH','IWD','IWA','LBH','LBD','LBA','PSH','PSD','PSA','WHH','WHD','WHA','VCH','VCD','VCA','Bb1X2','BbMxH','BbAvH','BbMxD','BbAvD','BbMxA','BbAvA','BbOU','BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5','BbAH','BbAHh','BbMxAHH','BbAvAHH','BbMxAHA','BbAvAHA']
	downloadReader = csv.DictReader(csvfile)
	downloadWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
	with open('E0.csv') as csvfile:
		mainReader = csv.DictReader(csvfile)
		for mainRow in mainReader:
			lastDate = mainRow['Date']
		lastDate = datetime.datetime.strptime(lastDate, '%d/%m/%y')
	with open('E0.csv', 'a') as csvfile:
		mainWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
		for downloadRow in downloadReader:
			if datetime.datetime.strptime(downloadRow['Date'], '%d/%m/%y') > lastDate:
				mainWriter.writerow(downloadRow)

homeOdds = []
awayOdds = []
drawOdds = []
homeGoals = []
awayGoals = []
homeGoalsConceded = []
awayGoalsConceded = []
homeShotsOnTarget = []
awayShotsOnTarget = []
homeShotsOnTargetFaced = []
awayShotsOnTargetFaced = []
totalHomeGoals = []
totalAwayGoals = []
homeTeam = input("Enter the Home Team: ")
awayTeam = input("Enter the Away Team: ")

nilNil = nilNilProb(homeTeam, awayTeam)

#collect data
with open('E0.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		totalHomeGoals.append(float(row['FTHG']))
		totalAwayGoals.append(float(row['FTAG']))
		if row['HomeTeam'] == homeTeam:
			homeGoals.append(float(row['FTHG']))
			homeShotsOnTarget.append(float(row['HST']))
			homeShotsOnTargetFaced.append(float(row['AST']))
			homeGoalsConceded.append(float(row['FTAG']))
		if row['AwayTeam'] == awayTeam:
			awayGoals.append(float(row['FTAG']))
			awayShotsOnTarget.append(float(row['AST']))
			awayShotsOnTargetFaced.append(float(row['HST']))
			awayGoalsConceded.append(float(row['FTHG']))
		if row['AwayTeam'] == awayTeam and row['HomeTeam'] == homeTeam:
			homeOdds.append(float(row['B365H']))
			awayOdds.append(float(row['B365A']))
			drawOdds.append(float(row['B365D']))

homeShotsOnTargetPerGoal = sum(homeShotsOnTarget)/sum(homeGoals)
awayShotsOnTargetPerGoal = sum(awayShotsOnTarget)/sum(awayGoals)
homeShotsOnTargetFacedPerGoal = sum(homeShotsOnTargetFaced)/sum(homeGoalsConceded)
awayShotsOnTargetFacedPerGoal = sum(awayShotsOnTargetFaced)/sum(awayGoalsConceded)

homeExpShotsOnTarget = (average(homeShotsOnTarget)+average(awayShotsOnTargetFaced))/2
awayExpShotsOnTarget = (average(awayShotsOnTarget)+average(homeShotsOnTargetFaced))/2

homeExpGoals = homeExpShotsOnTarget/((homeShotsOnTargetPerGoal+awayShotsOnTargetFacedPerGoal)/2)
awayExpGoals = awayExpShotsOnTarget/((awayShotsOnTargetPerGoal+homeShotsOnTargetFacedPerGoal)/2)

averageHomeOdds = average(homeOdds)
averageAwayOdds = average(awayOdds)
averageDrawOdds = average(drawOdds)
averageHomeGoals = average(homeGoals)
averageAwayGoals = average(awayGoals)

print(averageHomeGoals, averageAwayGoals)

probabilityMatrix = bivpois(10, 10, homeExpGoals, awayExpGoals, covariance(totalHomeGoals, totalAwayGoals), nilNil)

total = 0
homeProb = 0
awayProb = 0
drawProb = 0
for i in range(0,9):
	for j in range(0,9):
		#print(str(probabilityMatrix[i][j]) + ', ', end=" ")
		total += probabilityMatrix[i][j]
		if i > j:
			homeProb += probabilityMatrix[i][j]
		if i < j:
			awayProb += probabilityMatrix[i][j]
		if i == j:
			drawProb += probabilityMatrix[i][j]
	#print("\n")

homeProb = 1/homeProb
awayProb = 1/awayProb
drawProb = 1/drawProb
print(homeProb, drawProb, awayProb)
print(averageHomeOdds, averageDrawOdds, averageAwayOdds)
print(1/homeProb, 1/drawProb, 1/awayProb)
print(total)
print(covariance(totalHomeGoals, totalAwayGoals))
print(nilNil)
print(1/probabilityMatrix[1][1])