"""This is a Sodoku version, but only played out via text. Go to Sudoku_GUI to find the version
    with a user interface"""


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for t in range(len(board[i])):
            if t % 3 == 0 and t != 0:
                print("| ", end="")
            if t == 8:
                print(board[i][t])
            else:
                print(str(board[i][t]) + " ", end="")


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return i, j
    return None


def valid(board, row, col, val):
    """Method to check the validity of the row, col, and box of each entry"""
    # check the row
    for i in range(0, len(board)):
        if board[row][i] == val and col != i:
            return False
    # now let's check the col
    for i in range(0, len(board)):
        if board[i][col] == val and row != i:
            return False
    # now comes the tricky part, the boxes
    x = (col // 3) * 3
    y = (row // 3) * 3
    for i in range(y, y+3):
        for j in range(x, x+3):
            if board[i][j] == val and i != row and j != col:
                return False

    return True


"""def valid(board):
    # different method to check the validity, but it checks the whole board and uses binary numbers
    # create 3 vectors for the row, col, and block
    col = [0] * 9
    block = [0] * 9
    row = [0] * 9
    # visit each block once
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                idx = 1 << board[i][j]
                if row[i] & idx or col[j] & idx or block[i // 3 * 3 + j // 3] & idx:
                    return False
                row[i] |= idx
                col[j] |= idx
                block[i // 3 * 3 + j // 3] |= idx
    return True"""


def solve(board):
    """Solve the board"""
    pos = find_empty(board)
    if not pos:
        return True
    row, col = pos
    for i in range(1, 10):
        if valid(board, row, col, i):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0
    return False


def solvable(board):
    """Determines if the board is actually solvable"""
    pos = find_empty(board)
    if not pos:
        return True
    row, col = pos
    for i in range(1, 10):
        if valid(board, row, col, i):
            board[row][col] = i

            if solvable(board):
                board[row][col] = 0
                return True

            board[row][col] = 0
    return False


bo = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


"""print()
print_board(bo)
solvable(bo)
print("\n\n")
print_board(bo)"""
