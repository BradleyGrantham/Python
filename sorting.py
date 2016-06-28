sorted_combinedParameters = sorted(combinedParameters.items(), key=operator.itemgetter(1), reverse=True)
for item in sorted_combinedParameters:
	print(item)