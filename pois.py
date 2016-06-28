def pois(x, mean):
	result = ((mean ** x) * math.exp(- mean))/math.factorial(x)
	return result