from collections import OrderedDict
from copy import deepcopy
from math import pow
from time import clock

count = 0


class Node:
    def __init__(self, stateL, N, parentL, P, Pset, score, depth, action, area):
        self.state = stateL
        self.n = N
        self.parent = parentL
        self.p = P
        self.moves = Pset
        self.score = score
        self.depth = depth
        self.action = action
        self.area = area


class Eval:
    def __init__(self, max, i, j, area, actions):
        self.max = max
        self.actions = actions
        self.point = str(i) + ' ' + str(j)
        self.area = area


class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col


def printM(m):
    print
    for x in m:
        print x


def readfile(filename):
    file_input = open(filename, 'r')
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


def write_output(letter, number, matrix, time):
    file_output = open("output.txt", 'w')
    file_output.write(letter)
    file_output.write(number)
    file_output.write("\n")
    file_output.write(str(time))
    file_output.write("\n")
    # printM(matrix)
    for x in matrix:
        for a in x:
            file_output.write(str(a))
        file_output.write("\n")


def extract_point(s):
    i = s.find(' ')
    a = s[0:i]
    b = s[i + 1:]
    return Point(int(a), int(b))


def DFS(explored, P, state, n, fruitType, R):
    point = str(P.row) + ' ' + str(P.col)
    explored.add(point)
    R.add(str(P.row) + ' ' + str(P.col))
    # 1Q
    i = P.row - 1
    j = P.col
    if i >= 0 and j < n:
        is_explored = str(i) + ' ' + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R)
        else:
            explored.add(str(i) + ' ' + str(j))
    # 2Q
    i = P.row
    j = P.col - 1
    if i >= 0 and j >= 0:
        is_explored = str(i) + ' ' + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R)
        else:
            explored.add(str(i) + ' ' + str(j))
    # 3Q
    i = P.row + 1
    j = P.col
    if i < n and j >= 0:
        is_explored = str(i) + ' ' + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R)
        else:
            explored.add(str(i) + ' ' + str(j))
    # 4Q
    i = P.row
    j = P.col + 1
    if i < n and j < n:
        is_explored = str(i) + ' ' + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R)
        else:
            explored.add(str(i) + ' ' + str(j))
    return R


def eval_area(row, col, state, n):
    if row < 0 or row > n or col < 0 or col > n or state is None:
        return set()
    try:
        fruitType = state[row][col]
        if fruitType == '*':
            return set()  # invalid move
        else:
            A = DFS(set(), Point(row, col), state, n, fruitType, set())
            return A
    except IndexError:
        return set()


def eval(node):
    Pset = deepcopy(node.moves)
    maxL = 0
    a, b = -1, -1
    area = None
    actions = set()
    Pset_size = len(Pset)
    if Pset_size == 0:
        return Eval(maxL, 0, 0, area, actions)
    else:
        while len(Pset) != 0:
            point = Pset.pop()
            p = extract_point(point)
            i = p.row
            j = p.col
            current = eval_area(i, j, node.state, node.n)
            if len(current) != 0:
                max_candidate = int(pow(len(current), 2))
                if max_candidate >= maxL:
                    maxL = max_candidate
                    a = i
                    b = j
                    area = deepcopy(current)
                Pset -= current
                actions.add(current.pop())
        return Eval(maxL, a, b, area, actions)


def actions(node):
    Pset = deepcopy(node.moves)
    action_areas = dict()
    if len(Pset) == 0:
        return action_areas
    else:
        while len(Pset) != 0:
            point = Pset.pop()
            p = extract_point(point)
            i = p.row
            j = p.col
            current = eval_area(i, j, node.state, node.n)
            Pset -= current
            if len(current) != 0:
                ix = current.pop()
                current.add(ix)
                action_areas[ix] = current
        action_areas = OrderedDict(sorted(action_areas.items(), key=lambda t: len(t[1]), reverse=True))

        return action_areas


def push(v):
    a = []
    b = []
    for i in v:
        if i != '*':
            a.append(i)
        else:
            b.append(i)
    return b + a


def gravity(node, area, point, type):
    board = deepcopy(node.state)
    affected_columns = set()
    score = len(area)
    for x in area:
        p = extract_point(x)
        i = p.row
        j = p.col
        affected_columns.add(j)
        board[i][j] = '*'
    for x in affected_columns:
        column = [row[x] for row in board]
        column = push(column)
        for i in range(0, node.n):
            board[i][x] = column[i]
    pset = node.moves - area
    score = int(pow(score, 2))
    if type == 1:
        return Node(board, node.n, node, node.p, pset, node.score + score, node.depth + 1, point, area)
    else:
        return Node(board, node.n, node, node.p, pset, node.score - score, node.depth + 1, point, area)


def max_value(node, alpha, beta, cut):
    r = node

    acts = actions(node)
    if len(acts) == 0:
        return r
    if node.depth >= cut:
        return r
    v = -900
    i = 0
    s = len(acts)
    # print len(acts)
    for a in acts:
        i += 1
        new_node = gravity(node, acts[a], a, 1)
        ns = min_value(new_node, alpha, beta, cut)
        if v < ns.score:
            v = ns.score
            r = ns

        alpha = max(alpha, v)
        if i > float(s) * 0.9:
            return r
    return r


def min_value(node, alpha, beta, cut):
    r = node
    acts = actions(node)
    if len(acts) == 0:
        return r
    if node.depth >= cut:
        return r
    v = 900
    i = 0
    s = len(acts)
    for a in acts:
        i += 1
        new_node = gravity(node, acts[a], a, 0)
        ns = max_value(new_node, alpha, beta, cut)
        if ns.score < v:
            v = ns.score
            r = ns

        beta = min(beta, v)
        if i > float(s) * 0.9:
            return r
    return r


def printR(node):
    print 'Score:' + str(node.score)
    print "Move: " + node.action


def search(node, cut):
    c = node
    v = max_value(node, -900, 900, cut)
    while v.parent is not None:
        c = v
        v = v.parent
    return c


def what_cut(time, n):
    if time <= 0.1:
        return 0

    if n == 1 or n == 2:
        if time <= 0.2:
            return 3
        return 3
    elif n == 3:
        if time <= 0.2:
            return 3
        return 3
    elif n == 4:
        if time <= 0.8:
            return 3
        elif time <= 1:
            return 3
        elif time <= 2:
            return 3
        return 3
    elif n == 5:
        if time <= 0.8:
            return 2
        elif 0.8 < time <= 5:
            return 3
        elif 5 < time <= 30:
            return 3
        elif 30 < time <= 250:
            return 3
        else:
            return 3
    elif n == 6:
        if time <= 0.8:
            return 2
        elif 0.8 < time <= 5:
            return 3
        elif 5 < time <= 30:
            return 3
        elif 30 < time <= 200:
            return 3
        elif 200 < time <= 280:
            return 3
        else:
            return 3
    elif n == 7:
        if time <= 0.8:
            return 1
        elif 0.8 < time <= 5:
            return 2
        elif 5 < time <= 30:
            return 3
        else:
            return 3
    elif n == 8:
        if time <= 0.8:
            return 1
        elif 0.8 < time <= 5:
            return 2
        elif 5 < time <= 30:
            return 3
        elif time >= 280:
            return 3
        else:
            return 3
    elif n == 9:
        if time <= 0.8:
            return 0
        elif 0.8 < time < 30:
            return 2
        else:
            return 3
    elif n == 10:
        if time <= 0.8:
            return 0
        elif 0.8 < time < 30:
            return 2
        elif time >= 150:
            return 3
        else:
            return 3
    elif n == 11:
        if time <= 0.8:
            return 0
        elif 0.8 < time <= 5:
            return 1
        elif 5 < time <= 30:
            return 2
        elif time >= 250:
            return 3
        else:
            return 3
    elif n == 12:
        if time <= 0.8:
            return 0
        elif 0.8 < time <= 5:
            return 1
        elif time >= 180:
            return 3
        else:
            return 2
    elif n == 13 or n == 14 or n == 15:
        if time <= 0.8:
            return 0
        elif 0.8 < time < 5:
            return 1
        elif time >= 240:
            return 3
        else:
            return 2
    elif n == 16:
        if time <= 0.8:
            return 0
        elif 0.8 < time < 5:
            return 1
        else:
            return 2
    elif n == 17 or n == 18:
        if time <= 3:
            return 0
        elif 3 < time <= 10:
            return 1
        else:
            return 2
    elif n >= 19:
        if time <= 10:
            return 0
        elif 10 < time <= 100:
            return 1
        else:
            return 2
    else:
        return 0


# t0 = clock()
# init_param = readfile("input22.txt")
# cutoff = what_cut(init_param['time_left'], init_param['N'])
# initial_node = Node(init_param['board'], init_param['N'], None, init_param['P'], init_param['Pset'], 0, 0, None, set())
# print cutoff
# if cutoff == 0:
#     ev = eval(initial_node)
#     initial_node.action = ev.point
#     initial_node.score = ev.max
#     initial_node.area = ev.area
#     p = extract_point(initial_node.action)
#     i = p.row
#     j = p.col
#     initial_node.state = gravity(initial_node, eval_area(i, j, initial_node.state, initial_node.n), initial_node.action,
#                                  1).state
#     v = initial_node
# else:
#     v = search(initial_node, cutoff)
#
# p = extract_point(v.action)
# i = p.row
# j = p.col
# letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
#            'X', 'W', 'Y', 'Z']
# letter = letters[j]
#
# write_output(letter, str(i + 1), v.state, v.score)
#
