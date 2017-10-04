class Node:
    def __init__(self, stateL, N, parentL, P):
        self.state = stateL
        self.n = N
        self.parent = parentL
        self.p = P


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
                j += 1
        i += 1
    return dict(N=N, P=P, board=init_board, time_left=time_left)


def write_output(letter, number, matrix):
    file_output = open("output.txt", 'w')
    file_output.write(letter)
    file_output.write(number)
    file_output.write("\n")
    for x in matrix:
        for a in x:
            file_output.write(a)
        file_output.write("\n")


def DFS(explored, P, state, n, fruitType, R):
    explored.add(str(P.row) + str(P.col))
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


def eval_area(row, col, state, n, fruitType):
    fruitType = state[row][col]
    if fruitType == '*':
        return set()  # invalid move
    else:
        A = DFS(set(), Point(row, col), state, n, fruitType, set())
        return A


init_param = readfile("input5.txt")
initial_node = Node(init_param['board'], init_param['N'], None, init_param['P'])
printM(initial_node.state)
