import math
import numpy
import scipy
import csv
import urllib
import datetime
import os
import collections
import operator
import time
from collections import defaultdict
import random


def asianHandicap(probabilityMatrix):
	asianHandicap = {}
	homeProb = 0
	drawProb = 0
	awayProb = 0
	homeProbExactlyOne = 0
	homeProbExactlyTwo = 0
	awayProbExactlyOne = 0
	awayProbExactlyTwo = 0
	for i in range(0, 5):
		for j in range(0, 5):
			# print(str(probabilityMatrix[i][j]) + ', ', end=" ")
			if i > j:
				homeProb += probabilityMatrix[i][j]
			if i < j:
				awayProb += probabilityMatrix[i][j]
			if i == j:
				drawProb += probabilityMatrix[i][j]
			if i - j == 1:
				homeProbExactlyOne += probabilityMatrix[i][j]
			if i - j == 2:
				homeProbExactlyTwo += probabilityMatrix[i][j]
			if j - i == 1:
				awayProbExactlyOne += probabilityMatrix[i][j]
			if j - i == 2:
				awayProbExactlyTwo += probabilityMatrix[i][j]
			# print("\n")
	if homeProb > awayProb:
		asianHandicap['0'] = [round((1 - drawProb) / homeProb, 2),
							  round(1 / (1 - (1 / ((1 - drawProb) / homeProb))), 2)]
		asianHandicap['0.5'] = [round(1 / homeProb, 2), round(1 / (1 - homeProb), 2)]
	for handicap, odds in asianHandicap.items():
		print(handicap, odds)


def average(someList):
	answer = sum(someList) / len(someList)
	return answer


def pois(x, mean):
	result = ((mean ** x) * math.exp(- mean)) / math.factorial(x)
	return result


def bivpois(x, y, lambda1, lambda2, lambda3):
	extraProbabilityDraws = pois(0, x) * pois(0, y)
	if x == 0 or y == 0:
		probabilityMatrix = [[0 for i in range(x + 1)] for j in range(y + 1)]
		probabilityMatrix[x][y] = math.exp(- lambda3) * pois(x, lambda1) * pois(y, lambda2)
	else:
		probabilityMatrix = [[0 for i in range(x + 1)] for j in range(y + 1)]
		probabilityMatrix[0][0] = (1 - extraProbabilityDraws) * math.exp(-lambda1 - lambda2 - lambda3)
		for i in range(1, x + 1):
			probabilityMatrix[i][0] = (probabilityMatrix[i - 1][0] * lambda1) / (i)
		for j in range(1, y + 1):
			probabilityMatrix[0][j] = (probabilityMatrix[0][j - 1] * lambda2) / (j)
		for j in range(1, y + 1):
			for i in range(1, x + 1):
				probabilityMatrix[i][j] = (lambda1 * probabilityMatrix[i - 1][j] + lambda3 * probabilityMatrix[i - 1][j - 1]) / (i)
	probabilityMatrix[0][0] = probabilityMatrix[0][0] + pois(0, x) * pois(0, y)


	#print(extraProbabilityDraws)
	return probabilityMatrix


def covariance(homeGoals, awayGoals):
	averageHomeGoals = sum(homeGoals) / len(homeGoals)
	averageAwayGoals = sum(awayGoals) / len(awayGoals)
	covariance = 0
	for i in range(len(homeGoals)):
		covariance += (homeGoals[i] - averageHomeGoals) * (awayGoals[i] - averageAwayGoals)
	covariance = covariance / (len(homeGoals) - 1)
	return covariance


def nilNilProb(homeTeam, awayTeam):
	with open('E0.csv') as csvfile:
		count = 0
		nilNil = 0
		reader = csv.DictReader(csvfile)
		for row in reader:
			for team in top6:
				if row['HomeTeam'] == homeTeam and row['AwayTeam'] == team:
					count += 1
					if row['FTHG'] == '0' and row['FTAG'] == '0':
						nilNil += 1
				if row['HomeTeam'] == team and row['AwayTeam'] == homeTeam:
					count += 1
					if row['FTHG'] == '0' and row['FTAG'] == '0':
						nilNil += 1
				if row['HomeTeam'] == awayTeam and row['AwayTeam'] == team:
					count += 1
					if row['FTHG'] == '0' and row['FTAG'] == '0':
						nilNil += 1
				if row['HomeTeam'] == team and row['AwayTeam'] == awayTeam:
					count += 1
					if row['FTHG'] == '0' and row['FTAG'] == '0':
						nilNil += 1

	return nilNil / count


def predictor(probabilityMatrix):
	x = random.random()
	running_total = 0
	home_goals = 10
	away_goals = 10
	score = []
	for i in range(0, 5):
		for j in range(0, 5):
			# print(str(probabilityMatrix[i][j]) + ', ', end =" ")
			running_total += probabilityMatrix[i][j]
			if running_total > x:
				home_goals = i
				away_goals = j
				break
		if home_goals != 10 and away_goals != 10:
			break
	if home_goals == 10 and away_goals == 10:
		home_goals = 0
		away_goals = 0
	score = [home_goals, away_goals]
	return score

def ranking_metric(homeTeam, awayTeam, ranking):

	ppm = (ranking[homeTeam]-ranking[awayTeam])/100

	return ppm

def attack_grayson_rating(team, goalsFor, goalsAgainst, shotsFor, shotsAgainst, SoTFor, SoTAgainst, numberOfGames):
	GR = []
	TSR = []
	SoT_per_shot = []
	goalsForNew = goalsFor[team][-numberOfGames:]
	goalsAgainstNew = goalsAgainst[team][-numberOfGames:]
	shotsForNew = shotsFor[team][-numberOfGames:]
	shotsAgainstNew = shotsAgainst[team][-numberOfGames:]
	SoTForNew = SoTFor[team][-numberOfGames:]
	SoTAgainstNew = SoTAgainst[team][-numberOfGames:]
	for i in range(numberOfGames):
		if shotsForNew[i] == 0:
			SoT_per_shot.append(0)
		else:
			SoT_per_shot.append(SoTForNew[i]/shotsForNew[i])
	if sum(SoTForNew) == 0:
		goalConversion = 0
	else:
		goalConversion = sum(goalsForNew)/(sum(SoTForNew))
	if sum(SoTAgainstNew) == 0:
		goalConceded = 0
	else:
		goalConceded = sum(goalsAgainstNew)/sum(SoTAgainstNew)
	for i in range(numberOfGames):
		TSR.append(shotsForNew[i]/(shotsForNew[i]+shotsAgainstNew[i]))
	for i in range(numberOfGames):
		if goalsForNew[i]+goalsAgainstNew[i] == 0:
			GR.append(0)
		else:
			GR.append(goalsForNew[i]/(goalsForNew[i]+goalsAgainstNew[i]))
	TSoTR = sum(SoTForNew)/(sum(SoTForNew)+sum(SoTAgainstNew))
	#TSOTt = sum(SoTForNew)/sum(shotsForNew) + (sum(shotsAgainstNew)-sum(SoTAgainstNew))/sum(shotsAgainstNew)
	#PDO = 1000*(sum(goalsForNew)/sum(SoTForNew) + (sum(SoTAgainstNew)-sum(goalsAgainstNew))/sum(SoTAgainstNew))
	#rating = (0.5 + ((TSR-0.5)*math.pow(0.732,0.5)))*(1 + ((TSOTt-1)*math.pow(0.166,0.5)))*(1000 + ((PDO - 1000)*math.pow(0.176,0.5)))
	return average(TSR), average(SoT_per_shot), sum(goalsForNew)/sum(SoTForNew), average(GR)

def defence_grayson_rating(team, goalsFor, goalsAgainst, shotsFor, shotsAgainst, SoTFor, SoTAgainst, numberOfGames):
	GR_against = []
	TSR_against = []
	SoT_per_shot = []
	goalsForNew = goalsFor[team][-numberOfGames:]
	goalsAgainstNew = goalsAgainst[team][-numberOfGames:]
	shotsForNew = shotsFor[team][-numberOfGames:]
	shotsAgainstNew = shotsAgainst[team][-numberOfGames:]
	SoTForNew = SoTFor[team][-numberOfGames:]
	SoTAgainstNew = SoTAgainst[team][-numberOfGames:]
	for i in range(numberOfGames):
		if shotsAgainstNew[i] == 0:
			SoT_per_shot.append(0)
		else:
			SoT_per_shot.append(SoTAgainstNew[i]/shotsAgainstNew[i])
	if sum(SoTForNew) == 0:
		goalConversion = 0
	else:
		goalConversion = sum(goalsForNew)/(sum(SoTForNew))
	if sum(SoTAgainstNew) == 0:
		goalConceded = 0
	else:
		goalConceded = sum(goalsAgainstNew)/sum(SoTAgainstNew)
	for i in range(numberOfGames):
		TSR_against.append(shotsAgainstNew[i]/(shotsForNew[i]+shotsAgainstNew[i]))
	for i in range(numberOfGames):
		if goalsForNew[i]+goalsAgainstNew[i] == 0:
			GR_against.append(0)
		else:
			GR_against.append(goalsAgainstNew[i]/(goalsForNew[i]+goalsAgainstNew[i]))
	TSoTR = sum(SoTForNew)/(sum(SoTForNew)+sum(SoTAgainstNew))
	#TSOTt = sum(SoTForNew)/sum(shotsForNew) + (sum(shotsAgainstNew)-sum(SoTAgainstNew))/sum(shotsAgainstNew)
	#PDO = 1000*(sum(goalsForNew)/sum(SoTForNew) + (sum(SoTAgainstNew)-sum(goalsAgainstNew))/sum(SoTAgainstNew))
	#rating = (0.5 + ((TSR-0.5)*math.pow(0.732,0.5)))*(1 + ((TSOTt-1)*math.pow(0.166,0.5)))*(1000 + ((PDO - 1000)*math.pow(0.176,0.5)))
	return average(TSR_against), sum(goalsAgainstNew)/sum(SoTAgainstNew), average(goalsAgainstNew), average(GR_against)

'''#download new data
def downloadData():
	from urllib import request
	response = request.urlopen("http://www.football-data.co.uk/mmz4281/1516/E0.csv")
	downloadValues = response.read()
	csvstr = str(downloadValues).strip("b'")
	lines = csvstr.split("\\r\\n")
	with open('download.csv', 'w') as f:
		fieldnames = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A','BWH','BWD','BWA','IWH','IWD','IWA','LBH','LBD','LBA','PSH','PSD','PSA','WHH','WHD','WHA','VCH','VCD','VCA','Bb1X2','BbMxH','BbAvH','BbMxD','BbAvD','BbMxA','BbAvA','BbOU','BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5','BbAH','BbAHh','BbMxAHH','BbAvAHH','BbMxAHA','BbAvAHA', 'HomePenalties', 'AwayPenalties']
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		for line in lines[1:]:
			f.write(line + "\n")
downloadData()

#update data
with open('download.csv') as csvfile:
	fieldnames = ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A','BWH','BWD','BWA','IWH','IWD','IWA','LBH','LBD','LBA','PSH','PSD','PSA','WHH','WHD','WHA','VCH','VCD','VCA','Bb1X2','BbMxH','BbAvH','BbMxD','BbAvD','BbMxA','BbAvA','BbOU','BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5','BbAH','BbAHh','BbMxAHH','BbAvAHH','BbMxAHA','BbAvAHA','HomePenalties', 'AwayPenalties']
	downloadReader = csv.DictReader(csvfile)
	downloadWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
	with open('E0.csv') as csvfile:
		mainReader = csv.DictReader(csvfile)
		for mainRow in mainReader:
			lastDate = mainRow['Date']
		lastDate = datetime.datetime.strptime(lastDate, '%d/%m/%y')
	with open('E0.csv', 'a', newline='') as csvfile:
		mainWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
		csvfile.write('\n')
		for downloadRow in downloadReader:
			if datetime.datetime.strptime(downloadRow['Date'], '%d/%m/%y') > lastDate:
				mainWriter.writerow(downloadRow)

def updatePenalties():
	dict_date = {}
	dict_team = {}
	new_rows = []
	count = 0
	with open('Penalties.csv') as f:
		penalties_reader = csv.DictReader(f)
		for row in penalties_reader:
			if row['Scored or Missed'] == 'Scored':
				dict_date[float(row['Number'])] = row['Date']
				dict_team[float(row['Number'])] = row['Team']

	with open('E0.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			row['HomePenalties'] = '0'
			row['AwayPenalties'] = '0'
			new_rows.append(row)
			for number in range(len(dict_date)):
				if row['HomeTeam'] == dict_team[number] and row['Date'] == dict_date[number]:
					if row['HomePenalties'] == '3':
						row['HomePenalties'] = '4'
						new_rows.pop()
						new_rows.append(row)
					if row['HomePenalties'] == '2':
						row['HomePenalties'] = '3'
						new_rows.pop()
						new_rows.append(row)
					if row['HomePenalties'] == '1':
						row['HomePenalties'] = '2'
						new_rows.pop()
						new_rows.append(row)
					if row['HomePenalties'] == '0':
						row['HomePenalties'] = '1'
						new_rows.pop()
						new_rows.append(row)
				if row['AwayTeam'] == dict_team[number] and row['Date'] == dict_date[number]:
					if row['AwayPenalties'] == '3':
						row['AwayPenalties'] = '4'
						new_rows.pop()
						new_rows.append(row)
					if row['AwayPenalties'] == '2':
						row['AwayPenalties'] = '3'
						new_rows.pop()
						new_rows.append(row)
					if row['AwayPenalties'] == '1':
						row['AwayPenalties'] = '2'
						new_rows.pop()
						new_rows.append(row)
					if row['AwayPenalties'] == '0':
						row['AwayPenalties'] = '1'
						new_rows.pop()
						new_rows.append(row)

	with open('E0.csv', 'w') as f:
		writer = csv.DictWriter(f, ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A','BWH','BWD','BWA','IWH','IWD','IWA','LBH','LBD','LBA','PSH','PSD','PSA','WHH','WHD','WHA','SJH','SJD','SJA','VCH','VCD','VCA','Bb1X2','BbMxH','BbAvH','BbMxD','BbAvD','BbMxA','BbAvA','BbOU','BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5','BbAH','BbAHh','BbMxAHH','HomePenalties','AwayPenalties','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''])
		writer.writeheader()
		for row in new_rows:
			writer.writerow(row)
updatePenalties()'''

teams = set()
totalHomeGoals = []
totalAwayGoals = []
store_x = []
store_y = []
totalTeamPoints = defaultdict(list)
totalTeamPoints1 = defaultdict(list)
homeGoals = []
homeShots = []
homeShotsFaced = []
homeShotsOnTarget = []
homeShotsOnTargetFaced = []
awayGoals = []
awayShots = []
awayShotsFaced = []
awayShotsOnTarget = []
awayShotsOnTargetFaced = []
homeGoalsConc = []
awayGoalsConc = []
homeShotsOnTargetDict = defaultdict(list)
homeShotsOnTargetFacedDict = defaultdict(list)
homeGoalsDict = defaultdict(list)
homeGoalsConcDict = defaultdict(list)
homeShotsDict = defaultdict(list)
homeShotsFacedDict = defaultdict(list)
awayShotsOnTargetDict = defaultdict(list)
awayShotsOnTargetFacedDict = defaultdict(list)
awayGoalsDict = defaultdict(list)
awayGoalsConcDict = defaultdict(list)
awayShotsDict = defaultdict(list)
awayShotsFacedDict = defaultdict(list)
averageTeamPoints = defaultdict(list)
goalsDictNewSeasonAv = defaultdict(list)
totalGoalsDictNewSeason = defaultdict(list)



with open('E0.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		teams.add(row['HomeTeam'])

with open('E0.csv') as csvfile:
	for team in teams:
		reader = csv.DictReader(csvfile)
		csvfile.seek(0)
		for row in reader:
			if datetime.datetime.strptime(row['Date'], "%d/%m/%y") > datetime.datetime(2015, 6, 1) and datetime.datetime.strptime(row['Date'], "%d/%m/%y") < datetime.datetime(2016, 6, 1):
				totalHomeGoals.append((float(row['FTHG'])))
				totalAwayGoals.append((float(row['FTAG'])))
				if row['HomeTeam'] == team:
					homeShotsOnTargetDict[team].append(float(row['HST']))
					homeShotsOnTargetFacedDict[team].append(float(row['AST']))
					homeGoalsDict[team].append((float(row['FTHG'])))
					homeGoalsConcDict[team].append((float(row['FTAG'])))
					homeShotsDict[team].append((float(row['HS'])))
					homeShotsFacedDict[team].append((float(row['AS'])))
				if row['AwayTeam'] == team:
					awayShotsOnTargetDict[team].append(float(row['AST']))
					awayShotsOnTargetFacedDict[team].append(float(row['HST']))
					awayGoalsDict[team].append((float(row['FTAG'])))
					awayGoalsConcDict[team].append((float(row['FTHG'])))
					awayShotsDict[team].append((float(row['AS'])))
					awayShotsFacedDict[team].append((float(row['HS'])))


homeShotsOnTargetDict['Middlesbrough'] = homeShotsOnTargetDict['Aston Villa']
homeShotsOnTargetFacedDict['Middlesbrough'] = homeShotsOnTargetFacedDict['Aston Villa']
homeGoalsDict['Middlesbrough'] = homeGoalsDict['Aston Villa']
homeGoalsConcDict['Middlesbrough'] = homeGoalsConcDict['Aston Villa']
homeShotsDict['Middlesbrough'] = homeShotsDict['Aston Villa']
homeShotsFacedDict['Middlesbrough'] = homeShotsFacedDict['Aston Villa']
awayShotsOnTargetDict['Middlesbrough'] = awayShotsOnTargetDict['Aston Villa']
awayShotsOnTargetFacedDict['Middlesbrough'] = awayShotsOnTargetFacedDict['Aston Villa']
awayGoalsDict['Middlesbrough'] = awayGoalsDict['Aston Villa']
awayGoalsConcDict['Middlesbrough'] = awayGoalsConcDict['Aston Villa']
awayShotsDict['Middlesbrough'] = awayShotsDict['Aston Villa']
awayShotsFacedDict['Middlesbrough'] = awayShotsFacedDict['Aston Villa']

homeShotsOnTargetDict['Hull'] = homeShotsOnTargetDict['Aston Villa']
homeShotsOnTargetFacedDict['Hull'] = homeShotsOnTargetFacedDict['Aston Villa']
homeGoalsDict['Hull'] = homeGoalsDict['Aston Villa']
homeGoalsConcDict['Hull'] = homeGoalsConcDict['Aston Villa']
homeShotsDict['Hull'] = homeShotsDict['Aston Villa']
homeShotsFacedDict['Hull'] = homeShotsFacedDict['Aston Villa']
awayShotsOnTargetDict['Hull'] = awayShotsOnTargetDict['Aston Villa']
awayShotsOnTargetFacedDict['Hull'] = awayShotsOnTargetFacedDict['Aston Villa']
awayGoalsDict['Hull'] = awayGoalsDict['Aston Villa']
awayGoalsConcDict['Hull'] = awayGoalsConcDict['Aston Villa']
awayShotsDict['Hull'] = awayShotsDict['Aston Villa']
awayShotsFacedDict['Hull'] = awayShotsFacedDict['Aston Villa']

homeShotsOnTargetDict['Burnley'] = homeShotsOnTargetDict['Aston Villa']
homeShotsOnTargetFacedDict['Burnley'] = homeShotsOnTargetFacedDict['Aston Villa']
homeGoalsDict['Burnley'] = homeGoalsDict['Aston Villa']
homeGoalsConcDict['Burnley'] = homeGoalsConcDict['Aston Villa']
homeShotsDict['Burnley'] = homeShotsDict['Aston Villa']
homeShotsFacedDict['Burnley'] = homeShotsFacedDict['Aston Villa']
awayShotsOnTargetDict['Burnley'] = awayShotsOnTargetDict['Aston Villa']
awayShotsOnTargetFacedDict['Burnley'] = awayShotsOnTargetFacedDict['Aston Villa']
awayGoalsDict['Burnley'] = awayGoalsDict['Aston Villa']
awayGoalsConcDict['Burnley'] = awayGoalsConcDict['Aston Villa']
awayShotsDict['Burnley'] = awayShotsDict['Aston Villa']
awayShotsFacedDict['Burnley'] = awayShotsFacedDict['Aston Villa']

chances = 0
with open('E0.csv') as csvfile:
	for boom in range(0, 1):

		wages = { 'Man City': 2.08, 'Liverpool': 1.63, 'Chelsea': 2.31, 'Arsenal': 2.06, 'Everton': 0.80, 'Tottenham': 1.18, 'Man United': 2.17, 'Southampton': 0.64, 'Stoke': 0.77, 'Hull': 0.3, 'Burnley': 0.3, 'Swansea': 0.55, 'West Ham': 0.74, 'West Brom': 0.73, 'Middlesbrough': 0.3, 'Crystal Palace': 0.58, 'Leicester': 0.60, 'Sunderland': 0.76, 'Watford': 0.31, 'Bournemouth': 0.27}
		dates = []
		totalHomeGoalsNewSeason = []
		totalAwayGoalsNewSeason = []
		goalsDictNewSeason = defaultdict(list)
		

		teamPoints = defaultdict(list)
		combinedParameters = defaultdict(list)
		flags = 0
		flag = 0
		draws = 0

	
		reader = csv.DictReader(csvfile)
		csvfile.seek(0)
		for row in reader:
			total = 0
			homeProb = 0
			awayProb = 0
			drawProb = 0
			win = 0
			if datetime.datetime.strptime(row['Date'], "%d/%m/%y") > datetime.datetime(2016, 6,1) and datetime.datetime.strptime(row['Date'], "%d/%m/%y") < datetime.datetime(2017, 6, 1):
				homeTeam = row['HomeTeam']
				awayTeam = row['AwayTeam']
				home_attack_rating1, home_attack_rating2, home_attack_rating3, home_attack_rating4 = attack_grayson_rating(homeTeam, homeGoalsDict, homeGoalsConcDict, homeShotsDict, homeShotsFacedDict, homeShotsOnTargetDict, homeShotsOnTargetFacedDict, 19)
				home_defence_rating1, home_defence_rating2, home_defence_rating3, home_defence_rating4 = defence_grayson_rating(homeTeam, homeGoalsDict, homeGoalsConcDict, homeShotsDict, homeShotsFacedDict, homeShotsOnTargetDict, homeShotsOnTargetFacedDict, 19)
				away_attack_rating1, away_attack_rating2, away_attack_rating3, away_attack_rating4 = attack_grayson_rating(awayTeam, awayGoalsDict, awayGoalsConcDict, awayShotsDict, awayShotsFacedDict, awayShotsOnTargetDict, awayShotsOnTargetFacedDict, 19)
				away_defence_rating1, away_defence_rating2, away_defence_rating3, away_defence_rating4 = defence_grayson_rating(awayTeam, awayGoalsDict, awayGoalsConcDict, awayShotsDict, awayShotsFacedDict, awayShotsOnTargetDict, awayShotsOnTargetFacedDict, 19)
				x = 0.4182*home_attack_rating1 + 0.9073*home_attack_rating2 + 0.3586*home_attack_rating3 - 0.5467*home_attack_rating4 + 0.5019*away_defence_rating1 + 0.9585*away_defence_rating2 + 1.0234*away_defence_rating3 + 1.4081*away_defence_rating4 - 0.8
				y = 0.4182*away_attack_rating1 + 0.9073*away_attack_rating2 + 0.3586*away_attack_rating3 - 0.5467*away_attack_rating4 + 0.5019*home_defence_rating1 + 0.9585*home_defence_rating2 + 1.0234*home_defence_rating3 + 1.4081*home_defence_rating4 - 0.8
				extra = wages[homeTeam] - wages[awayTeam]
				if x > 2 or y > 2:
					chances +=1
					print(homeTeam, awayTeam)
				if homeTeam =='Chelsea' or homeTeam =='Arsenal' or homeTeam =='Man United' or homeTeam == 'Man City':
					y = 0
				#print(homeTeam,x,y,awayTeam)
				probabilityMatrix = bivpois(6, 6, x, y, -0.2)
				for i in range(0, 5):
					for j in range(0, 5):
						# print(str(probabilityMatrix[i][j]) + ', ', end=" ")
						total += probabilityMatrix[i][j]
						if i > j:
							homeProb += probabilityMatrix[i][j]
						if i < j:
							awayProb += probabilityMatrix[i][j]
						if i == j:
							drawProb += probabilityMatrix[i][j]
						# print("\n")
				score = predictor(probabilityMatrix)
				if score[0] > score[1]:
					teamPoints[homeTeam].append(3)
				if score[0] < score[1]:
					teamPoints[awayTeam].append(3)
				if score[0] == score[1]:
					teamPoints[homeTeam].append(1)
					teamPoints[awayTeam].append(1)
				
				

				'''goalsDictNewSeason[homeTeam].append(float(score[0]))
				goalsDictNewSeason[awayTeam].append(float(score[1]))
				# print(x, probableHomeGoals)
				# print(y, probableAwayGoals)
				homeShotsOnTargetDict[homeTeam].append(float(row['HST']))
				homeShotsOnTargetFacedDict[homeTeam].append(float(row['AST']))
				homeGoalsDict[homeTeam].append(score[0])
				homeGoalsConcDict[homeTeam].append(score[1])
				homeShotsDict[homeTeam].append((float(row['HS'])))
				homeShotsFacedDict[homeTeam].append((float(row['AS'])))

				awayShotsOnTargetDict[awayTeam].append(float(row['AST']))
				awayShotsOnTargetFacedDict[awayTeam].append(float(row['HST']))
				awayGoalsDict[awayTeam].append(score[1])
				awayGoalsConcDict[awayTeam].append(score[0])
				awayShotsDict[awayTeam].append((float(row['AS'])))
				awayShotsFacedDict[awayTeam].append((float(row['HS'])))'''
				

		for team in teamPoints:
			totalTeamPoints[team].append(sum(teamPoints[team]))
			totalGoalsDictNewSeason[team].append(sum(goalsDictNewSeason[team]))
		#print(boom, maxi, sum(teamPoints[maxi]))
		#time.sleep(2)
		#print(len(homeGoalsConcDict['Chelsea']))
		#print(flag)

for team in totalTeamPoints:
	averageTeamPoints[team] = average(totalTeamPoints[team])
	goalsDictNewSeasonAv[team] = average(totalGoalsDictNewSeason[team])


from operator import itemgetter

sorted_data = sorted(averageTeamPoints.items(), key=operator.itemgetter(1), reverse=True)
goalsDictNewSeasonAv_sorted = sorted(goalsDictNewSeasonAv.items(), key=operator.itemgetter(1), reverse=True)

for i in range(20):
	print(sorted_data[i], goalsDictNewSeasonAv_sorted[i])

total_average_points = 0
total_average_points_previous_season = 0

print(chances)

