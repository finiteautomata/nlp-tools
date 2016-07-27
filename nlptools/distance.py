import numpy as np

def levenshtein(w1, w2):
    """
    Calculates the edit-distance from w1 to w2
    """
    l1 = len(w1)
    l2 = len(w2)

    """
    This is the matrix to calculate with Dynamic Programming the distances
    from the substrings of w1 and w2

    distances[i, j] will be equal to the distance from w1[:i] to w2[:j]
    """
    distances = np.zeros([l1+1, l2+1])

    distances[0, :] = np.array(range(l2+1))

    for i in range(1, l1+1):
        distances[i, 0] = i

        for j in range(1, l2+1):
            """
            Now we set distance as the minimum between
                - distances[i, j-1] + 1: this is the case when you convert w1[:i] to w2[:j-1], and then you just add the last character
                - distances[i-i, j] + 1: exactly the same case
                - distances[i-1, j-1] + t: This is the case when you first convert w1[:i-1], to w2[:j-1]. Then, you have two choices depending on whether w1[i-1] == w2[j-1]. If that is the case, converting w1[:i-1] to w2[j-1] will suffice (you just don't touch the last character), so t equals 0. If the last characters are different, you have to edit that one, so t == 1.

                NOTE: Remember True == 1 and False == 0
            """

            distances[i, j] = min(1 + distances[i-1, j],
                1 + distances[i, j-1],
                distances[i-1, j-1] + 1 - (w1[i-1] == w2[j-1]))
    return distances[-1, -1]