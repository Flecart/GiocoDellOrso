# calcolo le distanze che poi saranno hardcodate
INFINITY = 10000
adjacent = [[1,2,3], #0
        [0,3,4],
        [0,3,6], #2
        [0,1,2,5],
        [1,7,8], #4
        [3,9,10,11],
        [2,12,13], #6
        [4,8,14],
        [7,4,14,9], #8
        [8, 10,5,15],
        [5,9,11,15],#10
        [5,10,15,12],
        [11,6,16,13],#12
        [6,12,16],
        [7,8,18],#14
        [9,10,11,17],
        [12,13,19], #16
        [15,18,19,20],
        [14,17,20], #18
        [16, 17, 20],
        [18, 17, 19]]

distances = [[INFINITY] * 21 for _ in range(21)]

for i in range(21):
    for j in range(21):
        if i == j:
            distances[i][j] = 0
        elif j in adjacent[i]:
            distances[i][j] = 1

# floyd warshall to calculate distances 
for k in range(21):
    for i in range(21):
        for j in range(21):
            if distances[i][j] > distances[i][k] + distances[k][j]:
                distances[i][j] = distances[i][k] + distances[k][j]

print(distances) 
