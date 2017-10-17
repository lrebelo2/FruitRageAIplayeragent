from copy import deepcopy
from random import randint
from random import sample
from time import clock
import homework
import homework2


class color:
    BOLD = '\033[1m'
    END = '\033[0m'


def readfile2():
    file_input = open("output2.txt", 'r')
    i = 1
    time_left = 0.0
    N, P = 0, 0
    Pset = set()
    flag_empty = True
    init_board = [[]]
    for line in file_input:
        if i == 1:
            N = int(line.strip())
            init_board = [[0 for x in range(N)] for y in range(N)]
        elif i == 2:
            P = int(line.strip())
        elif i == 3:
            time_left = float(line.strip())
        else:
            j = 0
            for char in line.strip():

                init_board[i - 4][j] = char
                if char != '*':
                    Pset.add(str(i - 4) + ' ' + str(j))
                j += 1
        i += 1
    return dict(N=N, P=P, board=init_board, time_left=time_left, Pset=Pset)


def write_output2(n, matrix, time, score):
    file_output = open("output2.txt", 'w')
    file_output.write(str(n))
    file_output.write("\n")
    file_output.write(str(score))
    file_output.write("\n")
    file_output.write(str(time))
    file_output.write("\n")
    # printM(matrix)
    for x in matrix:
        for a in x:
            file_output.write(str(a))
        file_output.write("\n")


def empty(m):
    flag = True
    for i in m:
        for x in i:
            if x != '*':
                flag = False
    return flag


def random_agent(node):
    Pset = deepcopy(node.moves)
    if len(Pset) == 0 or empty(node.state):
        node.score = 0
        return node
    a = sample(Pset, 1).pop()
    node.action = a
    p = homework.extract_point(a)
    i = p.row
    j = p.col
    area = homework.eval_area(i, j, node.state, node.n)
    node.area = area
    new_node = homework.gravity(node, area, a, 1)
    return new_node


def write_file(filename):
    file_input = open(filename, 'r')
    i = 1
    x = 0
    Pset = set()
    init_board = [[]]
    for line in file_input:
        if i == 1:
            N = int(line.strip())
            init_board = [[0 for x in range(N)] for y in range(N)]
            x += 1
        elif i == 2:
            P = int(line.strip())
            x += 1
        elif i == 3:
            time_left = float(line.strip())
            x += 1
        else:
            j = 0
            x += 1
            for char in line.strip():

                init_board[i - 4][j] = char
                if char != '*':
                    Pset.add(str(i - 4) + ' ' + str(j))
                j += 1
        i += 1

    file_output = open("output2.txt", 'w')
    file_output.write(str(N))
    file_output.write("\n")
    file_output.write(str(0))
    file_output.write("\n")
    file_output.write(str(time_left))
    file_output.write("\n")
    matrix = init_board
    # homework.printM(matrix)
    for x in matrix:
        for a in x:
            file_output.write(str(a))
        file_output.write("\n")


A = 0
B = 0
D = 0
games = 11
print 'minimax vs minimax no ab 3'
opponent = 'minimax'

for x in range(0, games):
    print x
    write_file("input6.txt")
    s = randint(0, 1)
    scoreA, scoreB = 0, 0
    empt = False
    while not empt:
        if s == 1:
            t0=clock()
            init_param = readfile2()
            initial_node = homework.Node(init_param['board'], init_param['N'], None, 4, init_param['Pset'], 0, 0, None,
                                         set())
            time=init_param['time_left']
            cutoff = homework.what_cut(init_param['time_left'], initial_node.n)
            if cutoff == 0:
                ev = homework.eval(initial_node)
                initial_node.action = ev.point
                initial_node.score = ev.max
                initial_node.area = ev.area
                p = homework.extract_point(initial_node.action)
                i = p.row
                j = p.col
                initial_node.state = homework.gravity(initial_node,
                                                      homework.eval_area(i, j, initial_node.state, initial_node.n),
                                                      initial_node.action,
                                                      1).state
                v = initial_node
            else:
                v = homework.search(initial_node, cutoff)
                p = homework.extract_point(v.action)
                i = p.row
                j = p.col

            scoreA += v.score
            s = 0
            time_left=time - (clock()-t0)
            empt = empty(v.state)
            if time_left <= 0:
                print 'No more Time!!!!'
                empt=True
                out = 1
        else:
            if opponent == 'random':
                t0 = clock()
                init_param = readfile2()
                initial_node = homework.Node(init_param['board'], init_param['N'], None, 4, init_param['Pset'], 0, 0,
                                             None, set())
                initial_node.score = 0
                time = init_param['time_left']
                v = random_agent(initial_node)
                if v.action is not None:
                    p = homework.extract_point(v.action)
                    i = p.row
                    j = p.col
                else:
                    i, j = 0, 0
                scoreB += v.score
                s = 1
                time_left = time - (clock() - t0)
                empt = empty(homework.gravity(v, homework.eval_area(i, j, v.state, v.n), v.action, 1).state)
                if time_left <= 0:
                    print 'No more Time!!!!'
                    empt = True
                    out = 0
            elif opponent == 'minimax':
                t0 = clock()
                init_param = readfile2()
                time = init_param['time_left']
                initial_node = homework2.Node(init_param['board'], init_param['N'], None, 4, init_param['Pset'], 0, 0,
                                              None, set())
                ev = homework2.eval(initial_node)
                initial_node.action = ev.point
                initial_node.score = ev.max
                cutoff = homework2.what_cut(init_param['time_left'], initial_node.n)
                if cutoff == 0:
                    ev = homework2.eval(initial_node)
                    initial_node.action = ev.point
                    initial_node.score = ev.max
                    initial_node.area = ev.area
                    p = homework2.extract_point(initial_node.action)
                    i = p.row
                    j = p.col
                    initial_node.state = homework2.gravity(initial_node,
                                                          homework2.eval_area(i, j, initial_node.state, initial_node.n),
                                                          initial_node.action,
                                                          1).state
                    v = initial_node
                else:
                    v = homework2.search(initial_node, cutoff)
                    p = homework2.extract_point(v.action)
                    i = p.row
                    j = p.col
                scoreB += v.score
                time_left = time - (clock() - t0)
                s = 1
                empt = empty(v.state)
                if time_left <= 0:
                    print 'No more Time!!!!'
                    empt = True
                    out = 0
        write_output2(v.n, v.state, time_left, v.score)
    if scoreA > scoreB:
        A += 1
    elif scoreA < scoreB:
        B += 1
    else:
        D += 1

if A > B:
    print color.BOLD + "Minimax wins: ", A, "Win percentage: ", 100 * A / games, "%" + color.END
else:
    print "Minimax wins: ", A, "Win percentage: ", 100 * A / games, "%"
if opponent == 'random':
    if B < A:
        print "Random wins: ", B, "Win percentage: ", 100 * B / games, "%"
    else:
        print color.BOLD + "Random wins: ", B, "Win percentage: ", 100 * B / games, "%" + color.END
else:
    if B < A:
        print "minimax no ab wins: ", B, "Win percentage: ", 100 * B / games, "%"
    else:
        print color.BOLD + "minimax no ab wins: ", B, "Win percentage: ", 100 * B / games, "%" + color.END
print "Draws: ", D
