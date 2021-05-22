import random
import numpy as np

def varNameGenerator(oneSet):
    name = ''
    while True:
        space = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        space += ([i.upper() for i in space])
        name = ''.join(random.choices(space, k=1))
        space += ['1','2','3','4','5','6','7','8','9','0']
        name += ''.join(random.choices(space, k=4))
        if name not in oneSet:
            oneSet.add(name)
            break                
    return name

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((2, size_y))
    for x in range(2):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        if x >= 2:
            matrix[x%2, 0] = x
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x%2,y] = min(
                    matrix[(x-1)%2, y] + 1,
                    matrix[(x-1)%2, y-1],
                    matrix[x%2, y-1] + 1
                )
            else:
                matrix [x%2,y] = min(
                    matrix[(x-1)%2,y] + 1,
                    matrix[(x-1)%2,y-1] + 1,
                    matrix[x%2,y-1] + 1
                )
    # print (matrix)
    return (matrix[(size_x - 1)%2, size_y - 1])
