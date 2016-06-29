import math
import numpy
import scipy
import csv
import urllib
import datetime
import os
import collections
import operator
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

def ranking_metric(homeTeam, awayTeam, ranking_dict):

    ranking_metric = (ranking_dict[homeTeam]-ranking_dict[awayTeam])/100

    return ranking_metric

def grayson_rating(team, goalsFor, goalsAgainst, shotsFor, shotsAgainst, SoTFor, SoTAgainst, numberOfPreviousGames):
    goalsForNew = goalsFor[team][-numberOfPreviousGames:]
    goalsAgainstNew = goalsAgainst[team][-numberOfPreviousGames:]
    shotsForNew = shotsFor[team][-numberOfPreviousGames:]
    shotsAgainstNew = shotsAgainst[team][-numberOfPreviousGames:]
    SoTForNew = SoTFor[team][-numberOfPreviousGames:]
    SoTAgainstNew = SoTAgainst[team][-numberOfPreviousGames:]
    TSR = sum(shotsForNew)/(sum(shotsForNew)+sum(shotsAgainstNew))
    TSOTt = sum(SoTForNew)/sum(shotsForNew) + (sum(shotsAgainstNew)-sum(SoTAgainstNew))/sum(shotsAgainstNew)
    PDO = 1000*(sum(goalsForNew)/sum(SoTForNew) + (sum(SoTAgainstNew)-sum(goalsAgainstNew))/sum(SoTAgainstNew))
    rating = TSR
    #rating = (0.5 + ((TSR-0.5)*math.pow(0.732,0.5)))*(1 + ((TSOTt-1)*math.pow(0.166,0.5)))*(1000 + ((PDO - 1000)*math.pow(0.176,0.5)))
    return rating

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
TSR = defaultdict(list)
TsoTt = defaultdict(list)
TsoTtaverage = defaultdict(list)
totalTeamPoints = defaultdict(list)
shotsOnTargetDict = defaultdict(list)
shotsOnTargetFacedDict = defaultdict(list)
goalsDict = defaultdict(list)
goalsConcDict = defaultdict(list)
shotsDict = defaultdict(list)
shotsFacedDict = defaultdict(list)
averageTeamPoints = defaultdict(list)
ranking_dict = { 'Man City': 86, 'Liverpool': 84, 'Chelsea': 82, 'Arsenal': 79, 'Everton': 72, 'Tottenham': 69, 'Man United': 64, 'Southampton': 56, 'Stoke': 50, 'Newcastle': 49, 'Crystal Palace': 45, 'Swansea': 42, 'West Ham': 40, 'Sunderland': 38, 'Aston Villa': 38, 'Hull': 37, 'West Brom': 36, 'Leicester': 36, 'QPR': 36, 'Burnley': 36}
rateform_dict = { 'Man City': 1600, 'Liverpool': 1562.7907, 'Chelsea': 1525.5814, 'Arsenal': 1469.76744, 'Everton': 1339.53488, 'Tottenham': 1283.72093, 'Man United': 1190.69767, 'Southampton': 1041.86047, 'Stoke': 930.232558, 'Newcastle': 911.627907, 'Crystal Palace': 837.209302, 'Swansea': 781.395349, 'West Ham': 744.186047, 'Sunderland': 706.976744, 'Aston Villa': 706.976744, 'Hull': 688.372093, 'West Brom': 669.767442, 'Leicester': 669.767442, 'QPR': 669.767442, 'Burnley': 669.767442}

with open('rsquared.csv', 'w') as csvfile:
    csvfile.write('Date')
    csvfile.write(',')
    csvfile.write('Expected')
    csvfile.write(',')
    csvfile.write('Actual')
    csvfile.write('\n')

with open('alldata.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        teams.add(row['HomeTeam'])

with open('alldata.csv') as csvfile:
    for team in teams:
        goals = []
        shotsOnTarget = []
        shotsOnTargetFaced = []
        goals = []
        goalsConc = []
        shots = []
        shotsFaced = []
        reader = csv.DictReader(csvfile)
        csvfile.seek(0)
        for row in reader:
            totalHomeGoals.append((float(row['FTHG'])))
            totalAwayGoals.append((float(row['FTAG'])))
            if row['HomeTeam'] == team:
                shotsOnTarget.append(float(row['HST']))
                shotsOnTargetFaced.append(float(row['AST']))
                goals.append((float(row['FTHG'])))
                goalsConc.append((float(row['FTAG'])))
                shots.append((float(row['HS'])))
                shotsFaced.append((float(row['AS'])))
                #TSR[team].append(float(row['HS'])/(float(row['HS'])+float(row['AS'])))
                #TsoTt[team].append(float(row['HST'])/float(row['HS'])-(float(row['AST']))/float(row['AS']))
            if row['AwayTeam'] == team:
                shotsOnTarget.append(float(row['AST']))
                shotsOnTargetFaced.append(float(row['HST']))
                goals.append((float(row['FTAG'])))
                goalsConc.append((float(row['FTHG'])))
                shots.append((float(row['AS'])))
                shotsFaced.append((float(row['HS'])))
                #TSR[team].append(float(row['AS'])/(float(row['HS'])+float(row['AS'])))
                #TsoTt[team].append(float(row['AST'])/float(row['AS'])-(float(row['HST']))/float(row['HS']))
        if len(goals) != 0:
            shotsOnTargetDict[team] = shotsOnTarget
            shotsOnTargetFacedDict[team] = shotsOnTargetFaced
            goalsDict[team] = goals
            goalsConcDict[team] = goalsConc
            shotsDict[team] = shots
            shotsFacedDict[team] = shotsFaced

with open('alldata.csv') as csvfile:

        ranking_dict_new = { 'Man City': 0, 'Liverpool': 0, 'Chelsea': 0, 'Arsenal': 0, 'Everton': 0, 'Tottenham': 0, 'Man United': 0, 'Southampton': 0, 'Stoke': 0, 'Newcastle': 0, 'Crystal Palace': 0, 'Swansea': 0, 'West Ham': 0, 'Sunderland': 0, 'Aston Villa': 0, 'Hull': 0, 'West Brom': 0, 'Leicester': 0, 'QPR': 0, 'Burnley': 0}
        dates = []
        totalHomeGoalsNewSeason = []
        totalAwayGoalsNewSeason = []
        teamPoints = defaultdict(list)
        homeShotsOnTargetDictNewSeason = defaultdict(list)
        awayShotsOnTargetDictNewSeason = defaultdict(list)
        homeShotsOnTargetFacedDictNewSeason = defaultdict(list)
        awayShotsOnTargetFacedDictNewSeason = defaultdict(list)
        homeGoalsDictNewSeason = defaultdict(list)
        awayGoalsDictNewSeason = defaultdict(list)
        homeGoalsConcDictNewSeason = defaultdict(list)
        awayGoalsConcDictNewSeason = defaultdict(list)
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
            homeTeam = row['HomeTeam']
            awayTeam = row['AwayTeam']
            '''if len(homeGoalsDict[homeTeam]) != 0 and len(awayGoalsDict[awayTeam]) != 0 and len(homeGoalsDict[homeTeam]) > 6 and len(awayGoalsDict[awayTeam]) > 6:
                if len(homeGoalsDictNewSeason[homeTeam]) == 0 or len(awayGoalsDictNewSeason[awayTeam]) == 0 or len(homeShotsOnTargetDictNewSeason[homeTeam]) == 0 or average(homeShotsOnTargetDictNewSeason[homeTeam]) == 0 or average(awayShotsOnTargetFacedDictNewSeason[awayTeam]) == 0 or average(awayShotsOnTargetDictNewSeason[awayTeam]) == 0:
                    homeTeamGoalsPerSoT = average(homeGoalsDict[homeTeam]) / average(homeShotsOnTargetDict[homeTeam])
                    awayGoalsConcPerSoT = average(awayGoalsConcDict[awayTeam]) / average(awayShotsOnTargetFacedDict[awayTeam])
                    expHomeGoalsPerSoT = (homeTeamGoalsPerSoT + awayGoalsConcPerSoT) / 2
                    homeTeamGoalsConcPerSoT = average(homeGoalsConcDict[homeTeam]) / average(homeShotsOnTargetFacedDict[homeTeam])
                    awayGoalsPerSoT = average(awayGoalsDict[awayTeam]) / average(awayShotsOnTargetDict[awayTeam])
                    expAwayGoalsPerSoT = (homeTeamGoalsConcPerSoT + awayGoalsPerSoT) / 2
                    expHomeSoT = (average(homeShotsOnTargetDict[homeTeam]) + average(awayShotsOnTargetFacedDict[awayTeam])) / 2
                    expAwaySoT = (average(homeShotsOnTargetFacedDict[homeTeam]) + average(awayShotsOnTargetDict[awayTeam])) / 2
                    x = expHomeGoalsPerSoT * expHomeSoT
                    y = expAwayGoalsPerSoT * expAwaySoT
                    probabilityMatrix = bivpois(6, 6, x, y, 0.1)
                else:
                    if len(homeGoalsDictNewSeason[homeTeam]) < 16 and len(awayGoalsDictNewSeason[awayTeam]) < 16:
                        homeTeamGoalsPerSoT = (1 - len(homeGoalsDictNewSeason[homeTeam]) * 0.0625) * (average(homeGoalsDict[homeTeam]) / average(homeShotsOnTargetDict[homeTeam])) + (len(homeGoalsDictNewSeason[homeTeam]) * 0.0625) * (average(homeGoalsDictNewSeason[homeTeam]) / average(homeShotsOnTargetDictNewSeason[homeTeam]))
                        awayGoalsConcPerSoT = (1 - len(awayGoalsDictNewSeason[awayTeam]) * 0.0625) * (average(awayGoalsConcDict[awayTeam]) / average(awayShotsOnTargetFacedDict[awayTeam])) + (len(awayGoalsDictNewSeason[awayTeam]) * 0.0625) * (average(awayGoalsConcDictNewSeason[awayTeam]) / average(awayShotsOnTargetFacedDictNewSeason[awayTeam]))
                        expHomeGoalsPerSoT = (homeTeamGoalsPerSoT + awayGoalsConcPerSoT) / 2
                        homeTeamGoalsConcPerSoT = (1 - len(homeGoalsDictNewSeason[homeTeam]) * 0.0625) * (average(homeGoalsConcDict[homeTeam]) / average(homeShotsOnTargetFacedDict[homeTeam])) + (len(homeGoalsDictNewSeason[homeTeam]) * 0.0625) * (average(homeGoalsConcDictNewSeason[homeTeam]) / average(homeShotsOnTargetFacedDictNewSeason[homeTeam]))
                        awayGoalsPerSoT = (1 - len(awayGoalsDictNewSeason[awayTeam]) * 0.0625) * (average(awayGoalsDict[awayTeam]) / average(awayShotsOnTargetDict[awayTeam])) + (len(awayGoalsDictNewSeason[awayTeam]) * 0.0625) * (average(awayGoalsDictNewSeason[awayTeam]) / average(awayShotsOnTargetDictNewSeason[awayTeam]))
                        expAwayGoalsPerSoT = (homeTeamGoalsConcPerSoT + awayGoalsPerSoT) / 2
                        expHomeSoT = ((1 - len(homeGoalsDictNewSeason[homeTeam]) * 0.0625) * (average(homeShotsOnTargetDict[homeTeam])) + (len(homeGoalsDictNewSeason[homeTeam]) * 0.0625) * (average(homeShotsOnTargetDictNewSeason[homeTeam])) + (1 - len(awayGoalsDictNewSeason[awayTeam]) * 0.0625) * (average(awayShotsOnTargetFacedDictNewSeason[awayTeam])) + (len(awayGoalsDictNewSeason[awayTeam]) * 0.0625) * (average(awayShotsOnTargetFacedDictNewSeason[awayTeam]))) / 2
                        expAwaySoT = ((1 - len(homeGoalsDictNewSeason[homeTeam]) * 0.0625) * (average(homeShotsOnTargetFacedDict[homeTeam])) + (len(homeGoalsDictNewSeason[homeTeam]) * 0.0625) * (average(homeShotsOnTargetFacedDictNewSeason[homeTeam])) + (1 - len(awayGoalsDictNewSeason[awayTeam]) * 0.0625) * (average(awayShotsOnTargetDictNewSeason[awayTeam])) + (len(awayGoalsDictNewSeason[awayTeam]) * 0.0625) * (average(awayShotsOnTargetDictNewSeason[awayTeam]))) / 2
                        x = expHomeGoalsPerSoT * expHomeSoT
                        y = expAwayGoalsPerSoT * expAwaySoT
                        ppm = ranking_metric(homeTeam, awayTeam, ranking_dict)
                    else:
                        homeTeamGoalsPerSoT = average(homeGoalsDictNewSeason[homeTeam]) / average(homeShotsOnTargetDictNewSeason[homeTeam])
                        awayGoalsConcPerSoT = average(awayGoalsConcDictNewSeason[awayTeam]) / average(awayShotsOnTargetFacedDictNewSeason[awayTeam])
                        expHomeGoalsPerSoT = (homeTeamGoalsPerSoT + awayGoalsConcPerSoT) / 2
                        homeTeamGoalsConcPerSoT = average(homeGoalsConcDictNewSeason[homeTeam]) / average(homeShotsOnTargetFacedDictNewSeason[homeTeam])
                        awayGoalsPerSoT = average(awayGoalsDictNewSeason[awayTeam]) / average(awayShotsOnTargetDictNewSeason[awayTeam])
                        expAwayGoalsPerSoT = (homeTeamGoalsConcPerSoT + awayGoalsPerSoT) / 2
                        expHomeSoT = (average(homeShotsOnTargetDictNewSeason[homeTeam]) + average(awayShotsOnTargetFacedDictNewSeason[awayTeam])) / 2
                        expAwaySoT = (average(homeShotsOnTargetFacedDictNewSeason[homeTeam]) + average(awayShotsOnTargetDictNewSeason[awayTeam])) / 2
                        x = expHomeGoalsPerSoT * expHomeSoT
                        y = expAwayGoalsPerSoT * expAwaySoT
                        ppm = ranking_metric(homeTeam, awayTeam, ranking_dict_new)
                    store_x.append(x)
                    store_y.append(y)
                    probabilityMatrix = bivpois(6, 6, x, y, 0.1)
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
                    ranking_dict_new[homeTeam] = ranking_dict_new[homeTeam] + 3
                if score[0] < score[1]:
                    teamPoints[awayTeam].append(3)
                    ranking_dict_new[awayTeam] = ranking_dict_new[awayTeam] + 3
                if score[0] == score[1]:
                    teamPoints[homeTeam].append(1)
                    teamPoints[awayTeam].append(1)
                    ranking_dict_new[homeTeam] = ranking_dict_new[homeTeam] + 1
                    ranking_dict_new[awayTeam] = ranking_dict_new[awayTeam] + 1'''

            '''homeShotsOnTargetDictNewSeason[homeTeam].append(float(row['HST']))
            awayShotsOnTargetDictNewSeason[awayTeam].append(float(row['AST']))
            homeShotsOnTargetFacedDictNewSeason[homeTeam].append(float(row['AST']))
            awayShotsOnTargetFacedDictNewSeason[awayTeam].append(float(row['HST']))
            homeGoalsDictNewSeason[homeTeam].append(float(score[0]))
            awayGoalsDictNewSeason[awayTeam].append(float(score[1]))
            homeGoalsConcDictNewSeason[homeTeam].append(float(score[1]))
            awayGoalsConcDictNewSeason[awayTeam].append(float(score[0]))
            totalHomeGoalsNewSeason.append(float(score[0]))
            totalAwayGoalsNewSeason.append(float(score[1]))'''
            if len(goalsDict[homeTeam]) > 7 and len(goalsDict[awayTeam]) > 7:
                home_rating = grayson_rating(homeTeam, goalsDict, goalsConcDict, shotsDict, shotsFacedDict, shotsOnTargetDict, shotsOnTargetFacedDict, 4)
                away_rating = grayson_rating(awayTeam, goalsDict, goalsConcDict, shotsDict, shotsFacedDict, shotsOnTargetDict, shotsOnTargetFacedDict, 4)
                '''x = -0.6283 + 0.004*grayson_rating(homeTeam, goalsDict, goalsConcDict, shotsDict, shotsFacedDict, shotsOnTargetDict, shotsOnTargetFacedDict)
                y = -0.6283 + 0.004*grayson_rating(awayTeam, goalsDict, goalsConcDict, shotsDict, shotsFacedDict, shotsOnTargetDict, shotsOnTargetFacedDict)
                x = x + 0.003*(rateform_dict[homeTeam]-rateform_dict[awayTeam])
                y = y + 0.003*(rateform_dict[awayTeam]-rateform_dict[homeTeam])'''
                with open('rsquared.csv', 'a') as csvfile:
                    csvfile.write(row['Date'])
                    csvfile.write(',')
                    csvfile.write(str(home_rating))
                    csvfile.write(',')
                    csvfile.write(str(float(row['FTHG'])))
                    csvfile.write('\n')
                    csvfile.write(row['Date'])
                    csvfile.write(',')
                    csvfile.write(str(away_rating))
                    csvfile.write(',')
                    csvfile.write(str(float(row['FTAG'])))
                    csvfile.write('\n')
            '''if row['FTHG'] > row['FTAG']:
                rateform_dict[homeTeam] = rateform_dict[homeTeam] + 0.05*rateform_dict[awayTeam]
                rateform_dict[awayTeam] = rateform_dict[awayTeam] - 0.05*rateform_dict[awayTeam]
            if row['FTHG'] < row['FTAG']:
                rateform_dict[awayTeam] = rateform_dict[awayTeam] + 0.07*rateform_dict[homeTeam]
                rateform_dict[homeTeam] = rateform_dict[homeTeam] - 0.07*rateform_dict[homeTeam]
            if row['FTHG'] == row['FTAG']:
                rateform_dict[awayTeam] = rateform_dict[awayTeam] - 0.05*rateform_dict[awayTeam] + (0.07*rateform_dict[homeTeam] + 0.05*rateform_dict[awayTeam])/2
                rateform_dict[homeTeam] = rateform_dict[homeTeam] - 0.07*rateform_dict[homeTeam] + (0.07*rateform_dict[homeTeam] + 0.05*rateform_dict[awayTeam])/2
            # print(x, probableHomeGoals)
            # print(y, probableAwayGoals)'''
            shotsOnTargetDict[homeTeam].append(float(row['HST']))
            shotsOnTargetFacedDict[homeTeam].append(float(row['AST']))
            goalsDict[homeTeam].append((float(row['FTHG'])))
            goalsConcDict[homeTeam].append((float(row['FTAG'])))
            shotsDict[homeTeam].append((float(row['HS'])))
            shotsFacedDict[homeTeam].append((float(row['AS'])))

            shotsOnTargetDict[awayTeam].append(float(row['AST']))
            shotsOnTargetFacedDict[awayTeam].append(float(row['HST']))
            goalsDict[awayTeam].append((float(row['FTAG'])))
            goalsConcDict[awayTeam].append((float(row['FTHG'])))
            shotsDict[awayTeam].append((float(row['AS'])))
            shotsFacedDict[awayTeam].append((float(row['HS'])))

        for team in teamPoints:
            totalTeamPoints[team].append(sum(teamPoints[team]))
        #print(boom)
        #print(flag)

for team in TsoTt:
    TsoTtaverage[team] = average(TsoTt[team])

from operator import itemgetter

sorted_data = sorted(TsoTtaverage.items(), key=operator.itemgetter(1), reverse=True)

total_average_points = 0
total_average_points_previous_season = 0
for team in averageTeamPoints:
    total_average_points += averageTeamPoints[team]
    total_average_points_previous_season += ranking_dict[team]

print(total_average_points, total_average_points_previous_season) 
print(ranking_dict)
