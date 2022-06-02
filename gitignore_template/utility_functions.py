
def levenshtein_distance(a: str, b: str) -> int:
	"""
	Calculate the Levenshtein distance between two strings.
	"""

	# NOTE (JB) Initialize the matrix
	matrix = [[0 for x in range(len(b) + 1)] for x in range(len(a) + 1)]

	# NOTE (JB) Fill the first row and column of the matrix
	for x in range(len(a) + 1):
		matrix[x][0] = x
	for y in range(len(b) + 1):
		matrix[0][y] = y

	# NOTE (JB) Fill the rest of the matrix
	for x in range(1, len(a) + 1):
		for y in range(1, len(b) + 1):
			if a[x - 1] == b[y - 1]:
				matrix[x][y] = matrix[x - 1][y - 1]
			else:
				matrix[x][y] = min(matrix[x - 1][y] + 1, matrix[x][y - 1] + 1, matrix[x - 1][y - 1] + 1)

	# NOTE (JB) Return the distance
	return matrix[len(a)][len(b)]
