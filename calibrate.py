from random import randint

from homework import *


class Stat:
    def __init__(self, N, time, cut):
        self.N = N
        self.cut = cut
        self.time = time


def write_calibrate(v):
    file_output = open("calibrate.txt", 'w')
    for s in v:
        file_output.write(str(s.N) + ',' + str(s.time) + ',' + str(s.cut))
        file_output.write("\n")


letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
           'U',
           'V',
           'X', 'W', 'Y', 'Z']
n = 26
N = 1
P = 5
Pset = set()
board = [[0 for x in range(N)] for y in range(N)]
for i in range(0, N):
    for j in range(0, N):
        c = randint(0, P)
        board[i][j] = c
        Pset.add(str(i) + ' ' + str(j))

initial_node = Node(board, N, None, P, Pset, 0, 0, None, set())

stats = []
for cutoff in range(0, ):
    t0 = clock()

    if cutoff == 0:
        ev = eval(initial_node)
        initial_node.action = ev.point
        initial_node.score = ev.max
        initial_node.area = ev.area
        p = extract_point(initial_node.action)
        i = p.row
        j = p.col
        initial_node.state = gravity(initial_node, eval_area(i, j, initial_node.state, initial_node.n),
                                     initial_node.action,
                                     1).state
        v = initial_node
    else:
        v = search(initial_node, cutoff)
        p = extract_point(v.action)
        i = p.row
        j = p.col

    letter = letters[j]
    write_output(letter, str(i + 1), v.state, v.score)
    time = clock() - t0
    stats.append(Stat(N, time, cutoff))
    print str(N) + ',' + str(time) + ',' + str(cutoff)
write_calibrate(stats)
