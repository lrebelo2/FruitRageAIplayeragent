class Node:
    def __init__(self, stateL, N, parentL, P):
        self.state = stateL
        self.n = N
        self.parent = parentL
        self.p = P


class Eval:
    def __init__(self, max, i, j, area):
        self.max = max
        self.i = i
        self.j = j
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
            file_output.write(a)
        file_output.write("\n")


def DFS(explored, P, state, n, fruitType, R, Pset):
    point = str(P.row) + str(P.col)
    explored.add(point)
    Pset.discard(point)
    R.add(str(P.row) + str(P.col))
    # 1Q
    i = P.row - 1
    j = P.col
    if i >= 0 and j < n:
        is_explored = str(i) + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R, Pset)
        else:
            explored.add(str(i) + str(j))
    # 2Q
    i = P.row
    j = P.col - 1
    if i >= 0 and j >= 0:
        is_explored = str(i) + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R, Pset)
        else:
            explored.add(str(i) + str(j))
    # 3Q
    i = P.row + 1
    j = P.col
    if i < n and j >= 0:
        is_explored = str(i) + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R, Pset)
        else:
            explored.add(str(i) + str(j))
    # 4Q
    i = P.row
    j = P.col + 1
    if i < n and j < n:
        is_explored = str(i) + str(j) in explored
        if state[i][j] == fruitType and not is_explored:
            R = R | DFS(explored, Point(i, j), state, n, fruitType, R, Pset)
        else:
            explored.add(str(i) + str(j))
    return R


def eval_area(row, col, state, n, Pset):
    fruitType = state[row][col]
    if fruitType == '*':
        return set()  # invalid move
    else:
        A = DFS(set(), Point(row, col), state, n, fruitType, set(), Pset)
        return A


def eval(Pset, node):
    maxL = 0
    a, b = -1, -1
    area = None
    Pset_size = len(Pset)
    if Pset_size == 0:
        return False
    else:
        ix = 0
        while len(Pset) != 0:
            ix += 1
            point = Pset.pop()
            i = int(point[0])
            j = int(point[1])
            current = eval_area(i, j, node.state, node.n, Pset)
            max_candidate = len(current)
            if max_candidate > maxL:
                maxL = max_candidate
                a = i
                b = j
                area = current
        return Eval(maxL, a, b, area)


init_param = readfile("input5.txt")
initial_node = Node(init_param['board'], init_param['N'], None, init_param['P'])
printM(initial_node.state)
Pset = init_param['Pset']
r = eval(Pset, initial_node)
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'X', 'W', 'Y', 'Z']
write_output(letters[2], str(4 + 1), initial_node.state)  # COLUMN,ROW,BOARD
