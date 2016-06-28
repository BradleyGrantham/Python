def asianHandicap(probabilityMatrix[][]):
	asianHandicap = {}
	for i in range(0,5):
		for j in range(0,5):
			#print(str(probabilityMatrix[i][j]) + ', ', end=" ")
			total += probabilityMatrix[i][j]
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
		#print("\n")
	if homeProb > awayProb:
		asianHandicap["0"] = [(1-drawProb)/homeProb, 1/(1-(1/(1-drawProb)/homeProb))]
	print(asianHandicap)