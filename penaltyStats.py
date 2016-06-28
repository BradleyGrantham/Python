import math
import numpy
import scipy
import csv
import urllib
import datetime
import os
import collections
import operator

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

print(dict_date, dict_team)
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
    writer = csv.DictWriter(f, ['Div','Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','Referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A','BWH','BWD','BWA','IWH','IWD','IWA','LBH','LBD','LBA','PSH','PSD','PSA','WHH','WHD','WHA','SJH','SJD','SJA','VCH','VCD','VCA','Bb1X2','BbMxH','BbAvH','BbMxD','BbAvD','BbMxA','BbAvA','BbOU','BbMx>2.5','BbAv>2.5','BbMx<2.5','BbAv<2.5','BbAH','BbAHh','BbMxAHH','BbAvAHH','BbMxAHA','BbAvAHA',,'HomePenalties','AwayPenalties','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''])
    writer.writeheader()
    for row in new_rows:
    	writer.writerow(row)

