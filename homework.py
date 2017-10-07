from copy import deepcopy
from math import pow


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
        self.point = str(i) + str(j)
        self.area = area


class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col


def printM(m):
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
                    Pset.add(str(i - 4) + str(j))
                j += 1
        i += 1
    return dict(N=N, P=P, board=init_board, time_left=time_left, Pset=Pset)


def write_output(letter, number, matrix):
    file_output = open("output.txt", 'w')
    file_output.write(letter)
    file_output.write(number)
    file_output.write("\n")
    for x in matrix:
        for a in x:
            file_output.write(str(a))
        file_output.write("\n")


def DFS(explored, P, state, n, fruitType, R):
    point = str(P.row) + str(P.col)
    explored.add(point)
    # Pset.discard(point)
    R.add(str(P.row) + str(P.col))
    # 1Q
    i = P.row - 1
    j = P.col
    if i >= 0 and j < n:
        is_explored = str(i) + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R)
        else:
            explored.add(str(i) + str(j))
    # 2Q
    i = P.row
    j = P.col - 1
    if i >= 0 and j >= 0:
        is_explored = str(i) + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R)
        else:
            explored.add(str(i) + str(j))
    # 3Q
    i = P.row + 1
    j = P.col
    if i < n and j >= 0:
        is_explored = str(i) + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R)
        else:
            explored.add(str(i) + str(j))
    # 4Q
    i = P.row
    j = P.col + 1
    if i < n and j < n:
        is_explored = str(i) + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R)
        else:
            explored.add(str(i) + str(j))
    return R


def eval_area(row, col, state, n):
    fruitType = state[row][col]
    if fruitType == '*':
        return set()  # invalid move
    else:
        A = DFS(set(), Point(row, col), state, n, fruitType, set())
        return A


def eval(node):
    Pset = moves(node.state)
    maxL = 0
    a, b = -1, -1
    area = None
    actions = set()
    Pset_size = len(Pset)
    if Pset_size == 0:
        return Eval(maxL, a, b, area, actions)
    else:
        while len(Pset) != 0:
            point = Pset.pop()
            i = int(point[0])
            j = int(point[1])
            current = eval_area(i, j, node.state, node.n)
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
            i = int(point[0])
            j = int(point[1])
            current = eval_area(i, j, node.state, node.n)
            if len(current) != 0:
                Pset -= current
                ix = current.pop()
                current.add(ix)
                action_areas[ix] = current
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


def moves(board):
    pset = set()
    n = len(board[0])
    for i in range(0, n):
        for j in range(0, n):
            if board[i][j] != '*':
                pset.add(str(i) + str(j))
    return pset


def gravity(node, area, point, type):
    board = deepcopy(node.state)
    affected_columns = set()
    score = len(area)
    for x in area:
        i = int(x[0])
        j = int(x[1])
        affected_columns.add(j)
        board[i][j] = '*'
    for x in affected_columns:
        column = [row[x] for row in board]
        column = push(column)
        for i in range(0, node.n):
            board[i][x] = column[i]
    pset = moves(board)
    score = int(pow(score, 2))
    if type == 1:
        return Node(board, node.n, node, node.p, pset, node.score + score, node.depth + 1, point, area)
    else:
        return Node(board, node.n, node, node.p, pset, node.score - score, node.depth + 1, point, area)


def max_value(node, alpha, beta, cut):
    acts = actions(node)
    if len(acts) == 0:
        return node
    if node.depth >= cut:
        return node
    v = -900
    # print len(acts)
    for a in acts:
        new_node = gravity(node, acts[a], a, 1)
        # print new_node.depth
        v = max(v, min_value(new_node, alpha, beta, cut).score)
        if v >= beta:
            return node
        alpha = max(alpha, v)
    return node


def min_value(node, alpha, beta, cut):
    acts = actions(node)
    if len(acts) == 0:
        return node
    if node.depth >= cut:
        return node
    v = 900
    for a in acts:
        new_node = gravity(node, acts[a], a, 0)
        v = min(v, max_value(new_node, alpha, beta, cut).score)
        if v <= alpha:
            return node
        beta = min(beta, v)
    return node


def printR(node):
    print 'Score:' + str(node.score)
    print "Move: " + node.action
    printM(node.state)


def search(node, cut):
    v = max_value(node, -900, 900, cut)
    printR(v)
    return v


init_param = readfile("input5.txt")
initial_node = Node(init_param['board'], init_param['N'], None, init_param['P'], init_param['Pset'], 0, 0, None, set())
# printM(initial_node.state)
cut = 2
ev = eval(initial_node)
initial_node.action = ev.point
initial_node.score = ev.max
v = search(initial_node, cut)
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'X', 'W', 'Y', 'Z']
i = int(v.action[0])
j = int(v.action[1])
letter = letters[j]
# printM(gravity(v,eval_area(i,j,v.state,v.n),v.action,0).state)
write_output(letter, str(i + 1), gravity(v, v.area, v.action, 0).state)
