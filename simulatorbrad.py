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


def asianHandicap(probability_matrix):
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
			# print(str(probability_matrix[i][j]) + ', ', end=" ")
			if i > j:
				homeProb += probability_matrix[i][j]
			if i < j:
				awayProb += probability_matrix[i][j]
			if i == j:
				drawProb += probability_matrix[i][j]
			if i - j == 1:
				homeProbExactlyOne += probability_matrix[i][j]
			if i - j == 2:
				homeProbExactlyTwo += probability_matrix[i][j]
			if j - i == 1:
				awayProbExactlyOne += probability_matrix[i][j]
			if j - i == 2:
				awayProbExactlyTwo += probability_matrix[i][j]
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
		probability_matrix = [[0 for i in range(x + 1)] for j in range(y + 1)]
		probability_matrix[x][y] = math.exp(- lambda3) * pois(x, lambda1) * pois(y, lambda2)
	else:
		probability_matrix = [[0 for i in range(x + 1)] for j in range(y + 1)]
		probability_matrix[0][0] = (1 - extraProbabilityDraws) * math.exp(-lambda1 - lambda2 - lambda3)
		for i in range(1, x + 1):
			probability_matrix[i][0] = (probability_matrix[i - 1][0] * lambda1) / (i)
		for j in range(1, y + 1):
			probability_matrix[0][j] = (probability_matrix[0][j - 1] * lambda2) / (j)
		for j in range(1, y + 1):
			for i in range(1, x + 1):
				probability_matrix[i][j] = (lambda1 * probability_matrix[i - 1][j] + lambda3 * probability_matrix[i - 1][j - 1]) / (i)
	probability_matrix[0][0] = probability_matrix[0][0] + pois(0, x) * pois(0, y)


	#print(extraProbabilityDraws)
	return probability_matrix

def covariance(homeGoals, awayGoals):
	averageHomeGoals = sum(homeGoals) / len(homeGoals)
	averageAwayGoals = sum(awayGoals) / len(awayGoals)
	covariance = 0
	for i in range(len(homeGoals)):
		covariance += (homeGoals[i] - averageHomeGoals) * (awayGoals[i] - averageAwayGoals)
	covariance = covariance / (len(homeGoals) - 1)
	return covariance

def predictor(probability_matrix):
	x = random.random()
	running_total = 0
	home_goals = 10
	away_goals = 10
	score = []
	for i in range(0, 5):
		for j in range(0, 5):
			# print(str(probability_matrix[i][j]) + ', ', end =" ")
			running_total += probability_matrix[i][j]
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

def attack_rating(team, goalsFor, goalsAgainst, shotsFor, shotsAgainst, SoTFor, SoTAgainst, numberOfGames):
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
	return [average(TSR), average(SoT_per_shot), sum(goalsForNew)/sum(SoTForNew), average(GR)]

def defence_rating(team, goalsFor, goalsAgainst, shotsFor, shotsAgainst, SoTFor, SoTAgainst, numberOfGames):
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
	return [average(TSR_against), sum(goalsAgainstNew)/sum(SoTAgainstNew), average(goalsAgainstNew), average(GR_against)]

def probability_calculator(probability_matrix):
	total = 0
	home_prob = 0
	away_prob = 0
	draw_prob = 0
	for i in range(0, 5):
		for j in range(0, 5):
			#print(str(probability_matrix[i][j]) + ', ',end = " ")
			total += probability_matrix[i][j]
			if i > j:
				home_prob += probability_matrix[i][j]
			if i < j:
				away_prob += probability_matrix[i][j]
			if i == j:
				draw_prob += probability_matrix[i][j]
			#print("\n")
	return home_prob, away_prob, draw_prob

def regression(attack_ratings, defence_ratings):
	mean = 0.4182*attack_ratings[0] + 0.9073*attack_ratings[1] + 0.3586*attack_ratings[2] - 0.5467*attack_ratings[3] + 0.5019*defence_ratings[0] + 0.9585*defence_ratings[1] + 1.0234*defence_ratings[2] + 1.4081*defence_ratings[3] - 0.8
	return mean

'''#download new data
def downloadData():
	from urllib import request
	response = request.urlopen("http://www.football-data.co.uk/mmz4281/1516/E0.csv")
	downloadValues = response.read()
	csvstr = str(downloadValues).strip("b'")
	lines = csvstr.split("\\r\\n")
	with open('download.csv', 'w') as f:
		fieldnames = ['Div','Date','home_team','away_team','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A','BWH','BWD','BWA','IWH','IWD','IWA','LBH','LBD','LBA','PSH','PSD','PSA','WHH','WHD','WHA','VCH','VCD','VCA','Bb1X2','BbMxH','BbAvH','BbMxD','BbAvD','BbMxA','BbAvA','BbOU','BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5','BbAH','BbAHh','BbMxAHH','BbAvAHH','BbMxAHA','BbAvAHA', 'HomePenalties', 'AwayPenalties']
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writeheader()
		for line in lines[1:]:
			f.write(line + "\n")
downloadData()

#update data
with open('download.csv') as csvfile:
	fieldnames = ['Div','Date','home_team','away_team','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A','BWH','BWD','BWA','IWH','IWD','IWA','LBH','LBD','LBA','PSH','PSD','PSA','WHH','WHD','WHA','VCH','VCD','VCA','Bb1X2','BbMxH','BbAvH','BbMxD','BbAvD','BbMxA','BbAvA','BbOU','BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5','BbAH','BbAHh','BbMxAHH','BbAvAHH','BbMxAHA','BbAvAHA','HomePenalties', 'AwayPenalties']
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
				if row['home_team'] == dict_team[number] and row['Date'] == dict_date[number]:
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
				if row['away_team'] == dict_team[number] and row['Date'] == dict_date[number]:
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
		writer = csv.DictWriter(f, ['Div','Date','home_team','away_team','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A','BWH','BWD','BWA','IWH','IWD','IWA','LBH','LBD','LBA','PSH','PSD','PSA','WHH','WHD','WHA','SJH','SJD','SJA','VCH','VCD','VCA','Bb1X2','BbMxH','BbAvH','BbMxD','BbAvD','BbMxA','BbAvA','BbOU','BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5','BbAH','BbAHh','BbMxAHH','HomePenalties','AwayPenalties','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''])
		writer.writeheader()
		for row in new_rows:
			writer.writerow(row)
updatePenalties()'''

teams = set()
total_home_goals = []
total_away_goals = []
store_x = []
store_y = []
total_team_points = defaultdict(list)
home_shots_on_target = defaultdict(list)
home_shots_on_target_faced = defaultdict(list)
home_goals_scored = defaultdict(list)
home_goals_conceded = defaultdict(list)
home_total_shots = defaultdict(list)
home_total_shots_faced = defaultdict(list)
away_shots_on_target = defaultdict(list)
away_shots_on_target_faced = defaultdict(list)
away_goals_scored = defaultdict(list)
away_goals_conceded = defaultdict(list)
away_total_shots = defaultdict(list)
away_total_shots_faced = defaultdict(list)
av_team_points = defaultdict(list)
av_goals_scored = defaultdict(list)
total_goals = defaultdict(list)

wages = { 'Man City': 2.08, 'Liverpool': 1.63, 'Chelsea': 2.31, 'Arsenal': 2.06, 'Everton': 0.80, 'Tottenham': 1.18, 'Man United': 2.17, 'Southampton': 0.64, 'Stoke': 0.77, 'Hull': 0.3, 'Burnley': 0.3, 'Swansea': 0.55, 'West Ham': 0.74, 'West Brom': 0.73, 'Cardiff': 0.3, 'Crystal Palace': 0.58, 'Leicester': 0.60, 'Sunderland': 0.76, 'Newcastle': 0.60, 'Aston Villa': 0.60, 'Norwich': 0.30, 'Fulham': 0.50}
promoted_teams = ['Middlesbrough', 'Hull', 'Burnley']

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
				total_home_goals.append((float(row['FTHG'])))
				total_away_goals.append((float(row['FTAG'])))
				if row['HomeTeam'] == team:
					home_shots_on_target[team].append(float(row['HST']))
					home_shots_on_target_faced[team].append(float(row['AST']))
					home_goals_scored[team].append((float(row['FTHG'])))
					home_goals_conceded[team].append((float(row['FTAG'])))
					home_total_shots[team].append((float(row['HS'])))
					home_total_shots_faced[team].append((float(row['AS'])))
				if row['AwayTeam'] == team:
					away_shots_on_target[team].append(float(row['AST']))
					away_shots_on_target_faced[team].append(float(row['HST']))
					away_goals_scored[team].append((float(row['FTAG'])))
					away_goals_conceded[team].append((float(row['FTHG'])))
					away_total_shots[team].append((float(row['AS'])))
					away_total_shots_faced[team].append((float(row['HS'])))

for promoted_team in promoted_teams:
	home_shots_on_target[promoted_team] = home_shots_on_target['Aston Villa']
	home_shots_on_target_faced[promoted_team] = home_shots_on_target_faced['Aston Villa']
	home_goals_scored[promoted_team] = home_goals_scored['Aston Villa']
	home_goals_conceded[promoted_team] = home_goals_conceded['Aston Villa']
	home_total_shots[promoted_team] = home_total_shots['Aston Villa']
	home_total_shots_faced[promoted_team] = home_total_shots_faced['Aston Villa']
	away_shots_on_target[promoted_team] = away_shots_on_target['Aston Villa']
	away_shots_on_target_faced[promoted_team] = away_shots_on_target_faced['Aston Villa']
	away_goals_scored[promoted_team] = away_goals_scored['Aston Villa']
	away_goals_conceded[promoted_team] = away_goals_conceded['Aston Villa']
	away_total_shots[promoted_team] = away_total_shots['Aston Villa']
	away_total_shots_faced[promoted_team] = away_total_shots_faced['Aston Villa']


with open('E0.csv') as csvfile:
	for monte_carlo_iteration in range(0, 100):

		goals_for_one_season = defaultdict(list)
		team_points = defaultdict(list)
		
		reader = csv.DictReader(csvfile)
		csvfile.seek(0)
		for row in reader:
			if datetime.datetime.strptime(row['Date'], "%d/%m/%y") > datetime.datetime(2016,6,1) and datetime.datetime.strptime(row['Date'], "%d/%m/%y") < datetime.datetime(2017, 6, 1):
				home_team = row['HomeTeam']
				away_team = row['AwayTeam']
				home_attack_ratings = attack_rating(home_team, home_goals_scored, home_goals_conceded, home_total_shots, home_total_shots_faced, home_shots_on_target, home_shots_on_target_faced, 19)
				home_defence_ratings = defence_rating(home_team, home_goals_scored, home_goals_conceded, home_total_shots, home_total_shots_faced, home_shots_on_target, home_shots_on_target_faced, 19)
				away_attack_ratings = attack_rating(away_team, away_goals_scored, away_goals_conceded, away_total_shots, away_total_shots_faced, away_shots_on_target, away_shots_on_target_faced, 19)
				away_defence_ratings = defence_rating(away_team, away_goals_scored, away_goals_conceded, away_total_shots, away_total_shots_faced, away_shots_on_target, away_shots_on_target_faced, 19)
				'''x = regression(home_attack_ratings, away_defence_ratings)
				y = regression(away_attack_ratings, home_defence_ratings)
				x = x + 0.25 * wages[home_team]
				y = y + 0.25 * wages[away_team]
				extra = wages[home_team] - wages[away_team]
				x = x + extra'''
				x = (wages[home_team] - wages[away_team])*0.342879 + 1.527607
				y = (wages[away_team] - wages[home_team])*0.342879 + 1.527607
				'''if home_team == 'Chelsea':
					print(home_team,x,y,away_team)'''
				probability_matrix = bivpois(6, 6, x, y, -0.2)
				home_prob, away_prob, draw_prob = probability_calculator(probability_matrix)
				score = predictor(probability_matrix)
				if score[0] > score[1]:
					team_points[home_team].append(3)
				if score[0] < score[1]:
					team_points[away_team].append(3)
				if score[0] == score[1]:
					team_points[home_team].append(1)
					team_points[away_team].append(1)

				goals_for_one_season[home_team].append(float(score[0]))
				goals_for_one_season[away_team].append(float(score[1]))

		for team in team_points:
			total_team_points[team].append(sum(team_points[team]))
			total_goals[team].append(sum(goals_for_one_season[team]))
		print(monte_carlo_iteration)

for team in total_team_points:
	av_team_points[team] = average(total_team_points[team])
	av_goals_scored[team] = average(total_goals[team])


from operator import itemgetter
sorted_points = sorted(av_team_points.items(), key=operator.itemgetter(1), reverse=True)
sorted_goals = sorted(av_goals_scored.items(), key=operator.itemgetter(1), reverse=True)

for i in range(20):
	print(sorted_points[i], sorted_goals[i])



