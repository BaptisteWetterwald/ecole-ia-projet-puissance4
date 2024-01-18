import tkinter as tk
from tkinter import ttk
import numpy as np
import random as rnd
from multiprocessing import Process, Queue

disk_color = ['white', 'red', 'orange']
disks = list()

player_type = ['human']
for i in range(42):
    player_type.append('AI: alpha-beta level '+str(i+1))


def alpha_beta_decision(board, turn, ai_level, queue, max_player, current_depth=0):
    alpha = -10
    beta = 10
    player = game.current_player()
    moves = board.get_possible_moves()
    best_move = moves[0]
    best_value = -10
    for move in board.get_possible_moves():
        new_board = board.copy()
        new_board.add_disk(move, max_player, False)
        print(new_board.grid)
        value = min_value(new_board, turn + 1, player%2 + 1, ai_level, alpha, beta, current_depth + 1)
        if value > best_value:
            best_value = value
            best_move = move
    queue.put(best_move)

def min_value(board, turn, player, ai_level, alpha, beta, current_depth):
    if board.check_victory():
        return 100
    if current_depth >= ai_level:
        return board.eval(2 - (turn % 2))
    value = 10
    moves = board.get_possible_moves()
    for move in moves:
        new_board = board.copy()
        new_board.add_disk(move, player, False)
        value = min(value, max_value(new_board, turn + 1, player%2 + 1, ai_level, alpha, beta, current_depth + 1))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value

def max_value(board, turn, player, ai_level, alpha, beta, current_depth):
    if board.check_victory():
        return -100
    if current_depth >= ai_level:
        return board.eval(2 - (turn % 2))
    value = -10
    moves = board.get_possible_moves()
    for move in moves:
        new_board = board.copy()
        new_board.add_disk(move, player, False)
        value = max(value, min_value(new_board, turn + 1, player%2 + 1, ai_level, alpha, beta, current_depth + 1))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value


class Board:
    grid = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])

    def eval(self, player):
        score = self.compute_score(player)
        opponent_score = self.compute_score(3 - player)
        return score - opponent_score

    def compute_score(self, player):
        score = 0
        # Horizontal alignment check
        for line in range(6):
            for horizontal_shift in range(4):
                if self.grid[horizontal_shift][line] == self.grid[horizontal_shift + 1][line] == \
                        self.grid[horizontal_shift + 2][line] == self.grid[horizontal_shift + 3][line] == player:
                    score += 1
        # Vertical alignment check
        for column in range(7):
            for vertical_shift in range(3):
                if self.grid[column][vertical_shift] == self.grid[column][vertical_shift + 1] == \
                        self.grid[column][vertical_shift + 2] == self.grid[column][vertical_shift + 3] == player:
                    score += 1
        # Diagonal alignment check
        for horizontal_shift in range(4):
            for vertical_shift in range(3):
                if self.grid[horizontal_shift][vertical_shift] == self.grid[horizontal_shift + 1][vertical_shift + 1] == \
                        self.grid[horizontal_shift + 2][vertical_shift + 2] == self.grid[horizontal_shift + 3][
                    vertical_shift + 3] == player:
                    score += 1
                elif self.grid[horizontal_shift][5 - vertical_shift] == self.grid[horizontal_shift + 1][
                    4 - vertical_shift] == \
                        self.grid[horizontal_shift + 2][3 - vertical_shift] == self.grid[horizontal_shift + 3][
                    2 - vertical_shift] == player:
                    score += 1
        return score

    def copy(self):
        new_board = Board()
        new_board.grid = np.array(self.grid, copy=True)
        return new_board

    def reinit(self):
        self.grid.fill(0)
        for i in range(7):
            for j in range(6):
                canvas1.itemconfig(disks[i][j], fill=disk_color[0])

    def get_possible_moves(self):
        possible_moves = list()
        if self.grid[3][5] == 0:
            possible_moves.append(3)
        for shift_from_center in range(1, 4):
            if self.grid[3 + shift_from_center][5] == 0:
                possible_moves.append(3 + shift_from_center)
            if self.grid[3 - shift_from_center][5] == 0:
                possible_moves.append(3 - shift_from_center)
        return possible_moves

    def add_disk(self, column, player, update_display=True):
        for j in range(6):
            if self.grid[column][j] == 0:
                break
        self.grid[column][j] = player
        if update_display:
            canvas1.itemconfig(disks[column][j], fill=disk_color[player])

    def column_filled(self, column):
        return self.grid[column][5] != 0

    def check_victory(self):
        # Horizontal alignment check
        for line in range(6):
            for horizontal_shift in range(4):
                if self.grid[horizontal_shift][line] == self.grid[horizontal_shift + 1][line] == \
                        self.grid[horizontal_shift + 2][line] == self.grid[horizontal_shift + 3][line] != 0:
                    return True
        # Vertical alignment check
        for column in range(7):
            for vertical_shift in range(3):
                if self.grid[column][vertical_shift] == self.grid[column][vertical_shift + 1] == \
                        self.grid[column][vertical_shift + 2] == self.grid[column][vertical_shift + 3] != 0:
                    return True
        # Diagonal alignment check
        for horizontal_shift in range(4):
            for vertical_shift in range(3):
                if self.grid[horizontal_shift][vertical_shift] == self.grid[horizontal_shift + 1][vertical_shift + 1] ==\
                        self.grid[horizontal_shift + 2][vertical_shift + 2] == self.grid[horizontal_shift + 3][vertical_shift + 3] != 0:
                    return True
                elif self.grid[horizontal_shift][5 - vertical_shift] == self.grid[horizontal_shift + 1][4 - vertical_shift] ==\
                        self.grid[horizontal_shift + 2][3 - vertical_shift] == self.grid[horizontal_shift + 3][2 - vertical_shift] != 0:
                    return True
        return False


class Connect4:

    def __init__(self):
        self.board = Board()
        self.human_turn = False
        self.turn = 1
        self.players = (0, 0)
        self.ai_move = Queue()

    def current_player(self):
        return 2 - (self.turn % 2)

    def launch(self):
        self.board.reinit()
        self.turn = 0
        information['fg'] = 'black'
        information['text'] = "Turn " + str(self.turn) + " - Player " + str(
            self.current_player()) + " is playing"
        self.human_turn = False
        self.players = (combobox_player1.current(), combobox_player2.current())
        self.handle_turn()

    def move(self, column):
        if not self.board.column_filled(column):
            self.board.add_disk(column, self.current_player())
            self.handle_turn()

    def click(self, event):
        if self.human_turn:
            column = event.x // row_width
            self.move(column)

    def ai_turn(self, ai_level):
        print("AI turn")
        p = Process(target=parallel_alpha_beta_decision, args=(self.board, self.turn, ai_level, self.ai_move, self.current_player(),))
        p.start()
        p.join(timeout=1)  # Adjust the timeout value as needed
        if p.is_alive():
            p.terminate()
            p.join()
            print("AI turn terminated")
        else:
            print("AI turn finished")
            best_value, best_move = self.ai_move.get()
            if best_move is not None:
                print("AI move is not None")
                self.move(best_move)
            else:
                print("AI move is None")
                self.ai_wait_for_move()

    def ai_wait_for_move(self):
        if not self.ai_move.empty():
            self.move(self.ai_move.get())
            print("AI move received")
        else:
            window.after(100, self.ai_wait_for_move)
            print("AI move not received")

    def handle_turn(self):
        self.human_turn = False
        if self.board.check_victory():
            information['fg'] = 'red'
            information['text'] = "Player " + str(self.current_player()) + " wins !"
            return
        elif self.turn >= 42:
            information['fg'] = 'red'
            information['text'] = "This a draw !"
            return
        self.turn = self.turn + 1
        information['text'] = "Turn " + str(self.turn) + " - Player " + str(
            self.current_player()) + " is playing"
        if self.players[self.current_player() - 1] != 0:
            self.human_turn = False
            self.ai_turn(self.players[self.current_player() - 1])
        else:
            self.human_turn = True
    
    def ai_turn(self, ai_level):
        p = Process(target=parallel_alpha_beta_decision, args=(self.board, self.turn, ai_level, self.ai_move, self.current_player(),))
        p.start()
        p.join(timeout=1)  # Adjust the timeout value as needed
        if p.is_alive():
            p.terminate()
            p.join()
        else:
            best_value, best_move = self.ai_move.get()
            if best_move is not None:
                self.move(best_move)
            else:
                self.ai_wait_for_move()


def parallel_alpha_beta_decision(board, turn, ai_level, queue, max_player, current_depth=0):
    alpha = -10
    beta = 10
    player = game.current_player()
    moves = board.get_possible_moves()
    best_move = moves[0]
    best_value = -10
    processes = []

    for move in board.get_possible_moves():
        new_board = board.copy()
        new_board.add_disk(move, max_player, False)
        process_args = (new_board, turn + 1, player % 2 + 1, ai_level, alpha, beta, current_depth + 1)
        p = Process(target=parallel_min_value_target, args=(process_args, queue))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    for _ in range(len(processes)):
        result = queue.get()
        if result[0] > best_value:
            best_value, best_move = result

    queue.put((best_value, best_move))

def parallel_min_value_target(args, queue):
    result = parallel_min_value(*args)
    queue.put(result)

def parallel_min_value(board, turn, player, ai_level, alpha, beta, current_depth):
    if board.check_victory():
        return 100, None
    if current_depth >= ai_level:
        return board.eval(2 - (turn % 2)), None  # Evaluate the board at the current depth
    value = 10
    moves = board.get_possible_moves()
    best_move = moves[0]
    for move in moves:
        new_board = board.copy()
        new_board.add_disk(move, player, False)
        value, _ = parallel_max_value(new_board, turn + 1, player%2 + 1, ai_level, alpha, beta, current_depth + 1)
        if value <= alpha:
            return value, None
        beta = min(beta, value)
        best_move = move
    return value, best_move

def parallel_max_value(board, turn, player, ai_level, alpha, beta, current_depth):
    if board.check_victory():
        return -100, None
    if current_depth >= ai_level:
        return board.eval(2 - (turn % 2)), None  # Evaluate the board at the current depth
    value = -10
    moves = board.get_possible_moves()
    best_move = moves[0]
    for move in moves:
        new_board = board.copy()
        new_board.add_disk(move, player, False)
        value, _ = parallel_min_value(new_board, turn + 1, player%2 + 1, ai_level, alpha, beta, current_depth + 1)
        if value >= beta:
            return value, None
        alpha = max(alpha, value)
        best_move = move
    return value, best_move

game = Connect4()

width = 700
row_width = width // 7
row_height = row_width
height = row_width * 6
row_margin = row_height // 10

window = tk.Tk()
window.title("Connect 4")
canvas1 = tk.Canvas(window, bg="blue", width=width, height=height)

for i in range(7):
    disks.append(list())
    for j in range(5, -1, -1):
        disks[i].append(canvas1.create_oval(row_margin + i * row_width, row_margin + j * row_height, (i + 1) * row_width - row_margin,
                            (j + 1) * row_height - row_margin, fill='white'))
canvas1.grid(row=0, column=0, columnspan=2)

information = tk.Label(window, text="")
information.grid(row=1, column=0, columnspan=2)

label_player1 = tk.Label(window, text="Player 1: ")
label_player1.grid(row=2, column=0)
combobox_player1 = ttk.Combobox(window, state='readonly')
combobox_player1.grid(row=2, column=1)

label_player2 = tk.Label(window, text="Player 2: ")
label_player2.grid(row=3, column=0)
combobox_player2 = ttk.Combobox(window, state='readonly')
combobox_player2.grid(row=3, column=1)

combobox_player1['values'] = player_type
combobox_player1.current(0)
combobox_player2['values'] = player_type
combobox_player2.current(6)

button2 = tk.Button(window, text='New game', command=game.launch)
button2.grid(row=4, column=0)

button = tk.Button(window, text='Quit', command=window.destroy)
button.grid(row=4, column=1)

# Mouse handling
canvas1.bind('<Button-1>', game.click)
window.mainloop()