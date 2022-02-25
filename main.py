import tkinter as tk
from tkinter import Canvas
import random
import time


class Cell:
    def __init__(self):
        self.is_alive = False
        self.is_alive_next = False


def update_canvas(board, canvas):
    size_x = 40
    size_y = 40
    canvas.delete("all")
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j].is_alive:
                canvas.create_rectangle(i * size_x, j * size_y, (i + 1) * size_x, (j + 1) * size_y, fill='yellow',
                                        outline='yellow')
            else:
                canvas.create_rectangle(i * size_x, j * size_y, (i + 1) * size_x, (j + 1) * size_y, fill='black',
                                        outline='black')


def random_init_board(board):
    for row in board:
        for cell in row:
            cell.is_alive = random.choice([True, False])


def random_init(board, canvas):
    random_init_board(board)
    update_canvas(board, canvas)


def clear_init_board(board):
    for row in board:
        for cell in row:
            cell.is_alive = False


def clear_init(board, canvas):
    clear_init_board(board)
    update_canvas(board, canvas)


def compute_next_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            number_of_neighbors = 0
            for x in range(i - 1, i + 2):
                for y in range(j - 1, j + 2):
                    if x in range(len(board)) and y in range(len(board[x])) \
                            and (x != i or y != j) and board[x][y].is_alive:
                        number_of_neighbors += 1
            if number_of_neighbors <= 1 or number_of_neighbors >= 4:
                board[i][j].is_alive_next = False
            elif number_of_neighbors == 2 and board[i][j].is_alive:
                board[i][j].is_alive_next = True
            elif number_of_neighbors == 3:
                board[i][j].is_alive_next = True


def update_next_board(board):
    for row in board:
        for cell in row:
            cell.is_alive = cell.is_alive_next


def next_iteration(board, canvas):
    compute_next_board(board)
    update_next_board(board)
    update_canvas(board, canvas)


stop_loop = True


def auto_iteration(board, canvas, count):
    global stop_loop
    if count == 0:
        stop_loop = False
    if stop_loop:
        return
    next_iteration(board, canvas)
    time.sleep(0.2)
    canvas.after(1, lambda: auto_iteration(board, canvas, count + 1))


def stop_button():
    global stop_loop
    stop_loop = True


def button_pressed(event, board, canvas):
    size_x = size_y = 40
    i = event.x // size_x
    j = event.y // size_x
    board[i][j].is_alive = not board[i][j].is_alive
    update_canvas(board, canvas)


if __name__ == "__main__":
    board = [[Cell() for i in range(20)] for j in range(20)]
    top = tk.Tk()
    top.title("Game Of Life")
    c = Canvas(top, bg="black", height=800, width=800)
    c.bind("<Button-1>", lambda event: button_pressed(event, board, c))
    c.pack()
    init_button = tk.Button(top, text="New Random Initialization", command=lambda: random_init(board, c))
    init_button.pack()
    clear_button = tk.Button(top, text="New Empty Initialization", command=lambda: clear_init(board, c))
    clear_button.pack()
    next_button = tk.Button(top, text="Next Iteration", command=lambda: next_iteration(board, c))
    next_button.pack()
    auto_button = tk.Button(top, text="Auto Iteration", command=lambda: auto_iteration(board, c, 0))
    auto_button.pack()
    stop_button = tk.Button(top, text="Stop Auto Iteration", command=stop_button)
    stop_button.pack()
    top.mainloop()
