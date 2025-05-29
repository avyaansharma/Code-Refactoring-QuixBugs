def levenshtein(source, target):
    n = len(source)
    m = len(target)

    # Create a matrix to store distances between prefixes of the strings
    distance = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    # Initialize first row and column
    for i in range(n + 1):
        distance[i][0] = i
    for j in range(m + 1):
        distance[0][j] = j

    # Calculate distances
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if source[i - 1] == target[j - 1]:
                cost = 0
            else:
                cost = 1

            distance[i][j] = min(
                distance[i - 1][j] + 1,  # Deletion
                distance[i][j - 1] + 1,  # Insertion
                distance[i - 1][j - 1] + cost  # Substitution
            )

    return distance[n][m]
"""
Levenshtein Distance


Calculates the Levenshtein distance between two strings.  The Levenshtein distance is defined as the minimum amount of single-character edits (either removing a character, adding a character, or changing a character) necessary to transform a source string into a target string.

Input:
    source: The string you begin with.
    target: The string to transform into.

Output:
    The Levenshtein distance between the source and target.

Example:
    electron can be transformed into neutron by removing the e, turning the l into n, and turning the c into u.
    >>> levenshtein(electron, neutron)
    3
"""
