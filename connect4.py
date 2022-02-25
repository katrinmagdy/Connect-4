from tkinter.constants import TRUE
import numpy as np
import pygame
import sys
import math
import tkinter as tk
import time
import networkx as nx
import matplotlib.pyplot as plt

# Some Constants
BLUE = (39, 104, 197)
OFF_WHITE = (245, 245, 245)
RED = (232, 71, 71)
YELLOW = (240, 216, 106)

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARESIZE = 100

PIECE_ONE = 1
PIECE_TWO = 2

# Global variables
start = False
score1 = 0
score2 = 0
k = 0
pruning = False

print("\nWelcome to connect 4 debugger\n"
      "Here will be the log for each step where O is the USER play and X is the COMPUTER play\n")


# ********************************************************* Methods  *******************************************************************
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for i in range(ROW_COUNT):
        if board[i][col] == 0:
            return i


# def print_board(board):
#     print(np.flip(board, 0))

def winning_move(board):
    # reset scores
    score1 = 0
    score2 = 0
    # Check horizontal locations for win
    for i in range(COLUMN_COUNT - 3):
        for j in range(ROW_COUNT):
            if board[j][i] == PIECE_ONE and board[j][i + 1] == PIECE_ONE and board[j][i + 2] == PIECE_ONE and board[j][
                i + 3] == PIECE_ONE:
                score1 = score1 + 1
            elif board[j][i] == PIECE_TWO and board[j][i + 1] == PIECE_TWO and board[j][i + 2] == PIECE_TWO and \
                    board[j][
                        i + 3] == PIECE_TWO:
                score2 = score2 + 1

    # Check vertical locations for win
    for i in range(COLUMN_COUNT):
        for j in range(ROW_COUNT - 3):
            if board[j][i] == PIECE_ONE and board[j + 1][i] == PIECE_ONE and board[j + 2][i] == PIECE_ONE and \
                    board[j + 3][
                        i] == PIECE_ONE:
                score1 = score1 + 1
            elif board[j][i] == PIECE_TWO and board[j + 1][i] == PIECE_TWO and board[j + 2][i] == PIECE_TWO and \
                    board[j + 3][
                        i] == PIECE_TWO:
                score2 = score2 + 1

    # Check positively sloped diaganols
    for i in range(COLUMN_COUNT - 3):
        for j in range(ROW_COUNT - 3):
            if board[j][i] == PIECE_ONE and board[j + 1][i + 1] == PIECE_ONE and board[j + 2][i + 2] == PIECE_ONE and \
                    board[j + 3][
                        i + 3] == PIECE_ONE:
                score1 = score1 + 1
            elif board[j][i] == PIECE_TWO and board[j + 1][i + 1] == PIECE_TWO and board[j + 2][i + 2] == PIECE_TWO and \
                    board[j + 3][
                        i + 3] == PIECE_TWO:
                score2 = score2 + 1

    # Check negatively sloped diaganols
    for i in range(COLUMN_COUNT - 3):
        for j in range(3, ROW_COUNT):
            if board[j][i] == PIECE_ONE and board[j - 1][i + 1] == PIECE_ONE and board[j - 2][i + 2] == PIECE_ONE and \
                    board[j - 3][
                        i + 3] == PIECE_ONE:
                score1 = score1 + 1
            elif board[j][i] == PIECE_TWO and board[j - 1][i + 1] == PIECE_TWO and board[j - 2][i + 2] == PIECE_TWO and \
                    board[j - 3][
                        i + 3] == PIECE_TWO:
                score2 = score2 + 1

    return score1, score2


def draw_board(board):
    pygame.draw.rect(screen, OFF_WHITE, (0, 0, COLUMN_COUNT * SQUARESIZE, SQUARESIZE))
    for i in range(COLUMN_COUNT):
        for j in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (i * SQUARESIZE, j * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, OFF_WHITE, (
                int(i * SQUARESIZE + SQUARESIZE / 2), int(j * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for i in range(COLUMN_COUNT):
        for j in range(ROW_COUNT):
            if board[j][i] == 1:
                pygame.draw.circle(screen, YELLOW, (
                    int(i * SQUARESIZE + SQUARESIZE / 2), height - int(j * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[j][i] == 2:
                pygame.draw.circle(screen, RED, (
                    int(i * SQUARESIZE + SQUARESIZE / 2), height - int(j * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    display_Score()
    pygame.display.update()


def display_Score():
    scoreFont = pygame.font.SysFont("monospace", 20, bold=True)
    label1 = scoreFont.render(f"Your Score = {score1} ", 1, YELLOW)
    label2 = scoreFont.render(f"Comp Score = {score2} ", 1, RED)
    screen.blit(label1, (500, 25))
    screen.blit(label2, (500, 55))
    screen.blit(label, (40, 30))
    # pygame.display.update()


def isFinish(board):
    for i in range(COLUMN_COUNT):
        if is_valid_location(board, i):
            return False
    return True


# def score_check(board):
#     score = 0
#     # Score center column
#     center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
#     center_count = center_array.count(2)
#     score += center_count * 3
#
#     # Score Horizontal
#     for r in range(ROW_COUNT):
#         row_array = [int(i) for i in list(board[r, :])]
#         for c in range(COLUMN_COUNT - 3):
#             window = row_array[c:c + 4]
#             score += window_check(window)
#
#     # Score Vertical
#     for c in range(COLUMN_COUNT):
#         col_array = [int(i) for i in list(board[:, c])]
#         for r in range(ROW_COUNT - 3):
#             window = col_array[r:r + 4]
#             score += window_check(window)
#
#     # Score posiive sloped diagonal
#     for r in range(ROW_COUNT - 3):
#         for c in range(COLUMN_COUNT - 3):
#             window = [board[r + i][c + i] for i in range(4)]
#             score += window_check(window)
#
#     for r in range(ROW_COUNT - 3):
#         for c in range(COLUMN_COUNT - 3):
#             window = [board[r + 3 - i][c + i] for i in range(4)]
#             score += window_check(window)
#
#     return score
#
#


root = tk.Tk(className='Connect 4')
pruning_var = tk.BooleanVar()
k_var = tk.IntVar()
check = False


def submit():
    global start
    global pruning
    global k
    start = True
    pruning = pruning_var.get()
    k = k_var.get()

    print("The pruning is : " + str(pruning))
    print("K= " + str(k))
    root.destroy()


def startwindow():
    root.geometry("300x200")
    root['bg'] = '#1a4685'
    title_label = tk.Label(root, text='Connect 4', font=('Times New Roman', 25, 'bold'), bg='#1a4685',
                           fg='#%02x%02x%02x' % YELLOW)
    prunning_label = tk.Label(root, text='Prunning', font=('Times New Roman', 15, 'bold'), bg='#1a4685',
                              fg='#%02x%02x%02x' % YELLOW)
    with_check = tk.Checkbutton(root, text="", padx=20, variable=pruning_var, bg='#1a4685', font=('bold'),
                                fg='#dcdcdc', activebackground='#1a4685', selectcolor='#1a4685')

    k_label = tk.Label(root, text='K value', font=('Times New Roman', 15, 'bold'), bg='#1a4685',
                       fg='#%02x%02x%02x' % YELLOW)
    k_entry = tk.Entry(root, textvariable=k_var, font=('monospace', 10, 'normal'), width=10)

    enter_btn = tk.Button(root, text='GO', command=submit, bg='#%02x%02x%02x' % OFF_WHITE,
                          fg='#%02x%02x%02x' % (0, 0, 0), font=('Times New Roman', 13, 'bold'), width=10)

    title_label.place(x=80, y=20)
    k_label.place(x=70, y=70)
    k_entry.place(x=170, y=75)
    prunning_label.place(x=70, y=100)
    with_check.place(x=150, y=103)
    enter_btn.place(x=100, y=140)
    root.mainloop()


def print_board_logs(entry, fw):
    board, score = entry[0], entry[1]
    for i in range(ROW_COUNT - 1, -1, -1):
        for j in range(COLUMN_COUNT):
            if j == 0:
                fw.write("|")
            if board[i][j] == 0:
                fw.write(" ")
            elif board[i][j] == 1:
                fw.write("O")
            else:
                fw.write("X")
            if j == COLUMN_COUNT - 1:
                fw.write("|\n")
    for i in range(ROW_COUNT + 3):
        fw.write("_")
    fw.write("   Heuristic Score : " + str(score) + "\n")


def print_logs(logs):
    fw_logs = open("logs.txt", "w")
    for i in range(len(logs) - 1, -1, -1):
        fw_logs.write("\nLevel #" + str(i) + "\n")
        for j in range(len(logs[i])):
            print_board_logs(logs[i][j], fw_logs)
        fw_logs.write("\n")
        for _ in range(40):
            fw_logs.write("-")
        fw_logs.write("")
    fw_logs.close()


class GraphVisualization:

    def __init__(self):
        self.visual = []
        self.poses = {}
        self.colormap = []

    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    def addNode(self, a, pos):
        self.poses[a] = pos
        if (pos[0] % 2 == 0):
            self.colormap.append('blue')

        if (pos[0] % 2 != 0):
            self.colormap.append('red')

    def haskey(self, a):
        if a in self.poses.keys():
            return True

        return False

    def visualize(self):
        G = nx.DiGraph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G, pos=self.poses, node_color=self.colormap)
        plt.show()


class log_tree_node:
    children = list()
    value = -404
    strr = ""

    def __init__(self):
        self.children = list()
        self.value = -404
        self.strr = ""


def check_two(element, num):
    zero = False
    for ch in element:
        if ch == "0":
            zero = True
            break
    if zero:
        count_boolean = False
        for ch in element:
            if ch == num and count_boolean:
                return True
            elif ch == num:
                count_boolean = True
    return False


def count_four_and_three_and_two(arr, num, weight4, weight3, weight2):
    score = 0
    # Counting horizontal
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT - 3):
            element = str(int(arr[i][j])) + str(int(arr[i][j + 1])) + str(int(arr[i][j + 2])) + str(int(arr[i][j + 3]))
            if element == num * 4:
                score += weight4
            elif element == "0" + num * 3 or element == num * 3 + "0" or element == num + "0" + 2 * num or element == num * 2 + "0" + num:
                score += weight3
            elif check_two(element, num):
                score += weight2
    # Counting vertical
    for j in range(COLUMN_COUNT):
        for i in range(ROW_COUNT - 3):
            element = str(int(arr[i][j])) + str(int(arr[i + 1][j])) + str(int(arr[i + 2][j])) + str(int(arr[i + 3][j]))
            if element == num * 4:
                score += weight4
            elif element == num * 3 + "0":
                score += weight3
            elif check_two(element, num):
                score += weight2
    # Counting diagonal right
    for i in range(ROW_COUNT - 3):
        for j in range(COLUMN_COUNT - 3):
            element = str(int(arr[i][j])) + str(int(arr[i + 1][j + 1])) + str(int(arr[i + 2][j + 2])) + str(
                int(arr[i + 3][j + 3]))
            if element == num * 4:
                score += weight4
            elif (element == "0" + num * 3) or (element == num * 3 + "0" and arr[i + 2][j + 3] != 0) \
                    or element == num + "0" + 2 * num or element == num * 2 + "0" + num:
                score += weight3
            elif check_two(element, num):
                score += weight2
    # Counting diagonal left
    for i in range(ROW_COUNT - 3):
        for j in range(COLUMN_COUNT - 1, COLUMN_COUNT - 5, -1):
            element = str(int(arr[i][j])) + str(int(arr[i + 1][j - 1])) + str(int(arr[i + 2][j - 2])) + str(
                int(arr[i + 3][j - 3]))
            if element == num * 4:
                score += weight4
            elif element == "0" + num * 3 or (element == num * 3 + "0" and arr[i + 2][j - 3] != 0) \
                    or element == num + "0" + 2 * num or element == num * 2 + "0" + num:
                score += weight3
            elif check_two(element, num):
                score += weight2
    return score


def count(board):
    score = 0
    arrayOfCenter = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = arrayOfCenter.count(2)
    score += center_count * 3
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + 4]
            score += window_check(window)

    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + 4]
            score += window_check(window)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += window_check(window)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += window_check(window)

    return score


def window_check(window):
    score = 0
    if window.count(2) == 4:
        score += 100
    if window.count(1) == 4:
        score -= 100
    elif window.count(2) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(2) == 2 and window.count(0) == 2:
        score += 2
    if window.count(1) == 3 and window.count(0) == 1:
        score -= 10
    return score


def prioritize_mid(arr):
    score = 0
    weights_dictionary = {1: 1, 2: 1, 3: 6, 4: 1, 5: 1}
    for j in range(1, 6):
        if arr[0][j] == 0 or arr[ROW_COUNT - 1][j] != 0:
            continue
        if arr[ROW_COUNT - 1][j] == 2:
            score += weights_dictionary.get(j)
        for i in range(ROW_COUNT - 1):
            if arr[i][j] == 2 and arr[i + 1][j] == 0:
                score += weights_dictionary.get(j)
                break
    return score


def heuristic_function(arr):
    score = 0
    score += count(arr)
    #score += count_four_and_three_and_two(arr, "1", -1000, -100, -5)
    #score += count_four_and_three_and_two(arr, "2", 1000, 100, 5)
    #score += prioritize_mid(arr)
    return score


# 6 Rows and 7 columns
# Returns all possible children list where each entry is a tuple.(Column Move, Child Array)
def get_children(board, turn):
    children = list()
    for j in [3, 4, 2, 5, 1, 6, 0]:
        for i in range(ROW_COUNT):
            if board[i][j] == 0:
                child = board.copy()
                child[i][j] = turn + 1
                children.append(child)
                break
    return children


# Turn = 1 (Computer's turn , Max)
# Turn = 0 (Player's turn , Min)
def min_max_procedure_no_pruning(board, k, turn, logs, parent):
    if k == 0:
        return heuristic_function(board)
    children = get_children(board, turn)
    for _ in range(len(children)):
        parent.children.append(log_tree_node())
    if not children:
        return heuristic_function(board)
    scores = list()
    for i in range(len(children)):
        scores.append(min_max_procedure_no_pruning(children[i], k - 1, 0, logs, parent.children[i]))
        parent.children[i].value = scores[i]
        logs[k - 1].append((children[i], scores[i]))
    if turn == 1:
        return max(scores)
    else:
        return min(scores)


def min_max_procedure_with_pruning(board, k, turn, logs, alpha, beta, parent):
    if k == 0:
        return heuristic_function(board)

    children = get_children(board, turn)
    if not children:
        return heuristic_function(board)

    scores = list()
    for i in range(len(children)):
        parent.children.append(log_tree_node())
        scores.append(
            min_max_procedure_with_pruning(children[i], k - 1, (turn + 1) % 2, logs, alpha, beta, parent.children[i]))
        parent.children[i].value = scores[i]
        logs[k - 1].append((children[i], scores[-1]))
        if turn == 0:  # Min turn i.e modify beta
            if scores != [] and scores[-1] < beta:
                beta = scores[-1]
            if alpha >= beta:  # Pruning condition
                return -1000000000
        else:  # Max turn i.e modify alpha
            if scores != [] and scores[-1] > alpha:
                alpha = scores[-1]
            if alpha >= beta:  # Pruning condition
                return 1000000000
    if turn == 0:
        return min(scores)
    else:
        return max(scores)


def get_col(board, scores):
    available_moves = list()
    for j in [3, 4, 2, 5, 1, 6, 0]:
        if board[ROW_COUNT - 1][j] == 0:
            available_moves.append(j)
    return available_moves[scores.index(max(scores))]


def min_max(board, k, pruning):
    start_time = time.time_ns()
    children = get_children(board, 1)
    logs = [list() for _ in range(k)]
    logs_root = log_tree_node()
    for _ in range(len(children)):
        logs_root.children.append(log_tree_node())
    scores = list()
    for i in range(len(children)):
        if pruning:
            scores.append(min_max_procedure_with_pruning(children[i], k - 1, 0, logs, -1000000000, 1000000000,
                                                         logs_root.children[i]))
        else:
            scores.append(min_max_procedure_no_pruning(children[i], k - 1, 0, logs, logs_root.children[i]))
        logs_root.children[i].value = scores[i]
        logs[k - 1].append((children[i], scores[i]))
    col = get_col(board, scores)
    logs_root.value = max(scores)
    G = GraphVisualization()

    x = 0
    y = 0
    const = 1
    queue = []
    temp = [logs_root, x, y]
    #queue.append(temp)
    while len(queue) > 0:
        temp = queue.pop(0)
        if temp[0].strr == "":
            temp[0].strr = "(" + str(temp[0].value) + ")"
        if G.haskey(temp[0].strr):
            temp[0].strr = str(const) + "(" + str(temp[0].value) + ")"
            const = const + 1
        G.addNode(temp[0].strr, (temp[1], temp[2]))
        xew = temp[1] + 1

        if (xew != x):
            x = xew
            y = 0

        for i in range(len(temp[0].children)):
            temp2 = [temp[0].children[i], xew, y]
            queue.append(temp2)
            y = y + 1

    queue = []
    queue.append(logs_root)
    while len(queue) > 0:
        temp = queue.pop(0)

        for i in range(len(temp.children)):
            temp2 = temp.children[i]
            queue.append(temp2)
            G.addEdge(temp.strr, temp.children[i].strr)

    #G.visualize()
    nodes_expanded = 0
    for log in logs:
        nodes_expanded += len(log)
    print("Execution time : " + str((time.time_ns() - start_time) / 1000000000) + " secs")
    print("Nodes Expanded : " + str(nodes_expanded))
    print_logs(logs)
    row = get_next_open_row(board, col)
    drop_piece(board, row, col, 2)
    (score1, score2) = winning_move(board)
    return score1, score2


# ********************************************************* MAIN *******************************************************************
startwindow()
if start:
    board = create_board()
    # print_board(board)
    game_over = False
    turn = 0

    pygame.init()

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    size = (width, height)

    RADIUS = int(SQUARESIZE / 2 - 5)
    myfont = pygame.font.SysFont("Times New Roman", 40, bold=True)
    label = myfont.render(f"", 1, YELLOW)
    screen = pygame.display.set_mode(size)
    draw_board(board)
    # display_Score()
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            display_Score()
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, OFF_WHITE, (0, 0, width, SQUARESIZE))  ####
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, OFF_WHITE, (0, 0, width, SQUARESIZE))  ######

                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    (score1, score2) = winning_move(board)
                else:
                    continue

                draw_board(board)  # Can be removed
                turn = 1

                if isFinish(board):
                    (score1, score2) = winning_move(board)
                    if score1 < score2:
                        label = myfont.render(f"Computer wins! ", 1, RED)
                    elif score2 < score1:
                        label = myfont.render(f"You wins! ", 1, YELLOW)
                    else:
                        label = myfont.render(f"It's a draw! ", 1, BLUE)
                    game_over = True
                    break

                score1, score2 = min_max(board, k, pruning)

                if isFinish(board):
                    (score1, score2) = winning_move(board)
                    if score1 < score2:
                        label = myfont.render(f"Computer wins! ", 1, RED)
                    elif score2 < score1:
                        label = myfont.render(f"You wins! ", 1, YELLOW)
                    else:
                        label = myfont.render(f"It's a draw! ", 1, BLUE)
                    game_over = True

                    # print_board(board)
                # display_Score(board)
                draw_board(board)
                turn = 0

    draw_board(board)
    # display_Score(board)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
