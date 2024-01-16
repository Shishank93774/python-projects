import math
import random
from queue import Queue

directions = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]


class TextColor:
    RESET = "\033[0m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"

class Board:
    def __init__(self, size):
        self.size = size
        self.bombs = list(random.sample(range(0, size * size - 1),
                                        random.choice(range(int(0.10 * size * size), int(0.15 * size * size)))))
        self.board = [[0 for _ in range(size)] for _t in range(size)]
        self.vis = set()
        self.bombSize = len(self.bombs)
        self.flag = set()

    def __str__(self):
        n = self.size
        print(f"\n\n🚩: {self.bombSize - len(self.flag)}")
        visible_board = [[None for _ in range(n)] for _ in range(n)]
        for row in range(n):
            for col in range(n):
                idx = row*n + col
                if idx in self.vis:
                    if self.board[row][col] == -1:
                        visible_board[row][col] = 'X'
                    else:
                        visible_board[row][col] = str(self.board[row][col])
                elif idx in self.flag:
                    visible_board[row][col] = '🚩'
                else:
                    visible_board[row][col] = ' '
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(n):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )
        for row in range(n):
            for col in range(n):
                idx = row*n + col
                if idx in self.vis:
                    if self.board[row][col] == 1:
                        visible_board[row][col] = f"{TextColor.BLUE}{str(1)}{TextColor.RESET}"
                    elif self.board[row][col] == 2:
                        visible_board[row][col] = f"{TextColor.GREEN}{str(2)}{TextColor.RESET}"
                    elif self.board[row][col] == 3:
                        visible_board[row][col] = f"{TextColor.RED}{str(3)}{TextColor.RESET}"
                    elif self.board[row][col] == 4:
                        visible_board[row][col] = f"{TextColor.PURPLE}{str(4)}{TextColor.RESET}"

        # print the csv strings
        indices = [i for i in range(n)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            form = '%-' + str(widths[idx]) + "s"
            cells.append(form % col)
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                form = '%-' + str(widths[idx]) + "s"
                cells.append(form % col)
            string_rep += " |".join(cells)
            string_rep += ' |\n'
        string_rep = string_rep.replace('🚩 ', '🚩')

        str_len = int(len(string_rep) / n)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len + '\n\n'

        return string_rep

    def initialize_board(self):
        bombs = self.bombs
        n = self.size
        for bomb in bombs:
            x = bomb // n
            y = bomb % n
            self.board[x][y] = -1
            for (dx, dy) in directions:
                tx = x + dx
                ty = y + dy
                tidx = tx * n + ty
                if tx < 0 or ty < 0 or tx == n or ty == n or tidx in bombs:
                    continue
                self.board[tx][ty] += 1
        # print(self.vis)

    def reveal_bombs(self):
        n = self.size
        for bomb in self.bombs:
            self.vis.add(bomb)

    def make_move(self, x, y, mode):
        n = self.size
        idx = x * n + y
        if mode == str(2):  # flagging mode
            if idx in self.flag:
                self.flag.remove(idx)
            else:
                if len(self.flag) == self.bombSize:
                    print("Flagging limit reached, please remove some flags.")
                    return True
                if idx in self.vis:
                    print("It's already exposed. Chill!!")
                    return True
                self.flag.add(idx)
            return True

        if idx in self.flag:
            ch = input("You have flagged this, wanna continue? y/n: ")
            if ch.lower() == 'n':
                return True
            self.flag.remove(idx)
        # if clicked on the bombs
        if idx in self.bombs:
            print("You are wrecked!!!")
            self.reveal_bombs()
            return False
        # if clicked on the visited cell
        if idx in self.vis:
            print("It's already exposed. Chill!!")
            return True
        # if clicked for the first time
        if idx not in self.vis:
            self.vis.add(idx)
            # if it's not zero
            if self.board[x][y] > 0:
                return True
            qu = Queue()
            qu.put(idx)
            while not qu.empty():
                u = qu.get()
                cx = u // n
                cy = u % n
                for (dx, dy) in directions:
                    tx = cx + dx
                    ty = cy + dy
                    tidx = tx * n + ty
                    if tx < 0 or ty < 0 or tx == n or ty == n or tidx in self.vis:
                        continue
                    if self.board[tx][ty] == 0:
                        qu.put(tidx)
                    self.vis.add(tidx)
            return True


def play_minesweeper(board):
    board.initialize_board()
    print(board)
    n = board.size
    while len(board.vis) + len(board.flag) < n * n:
        mode = None
        while mode != str(1) and mode != str(2):
            mode = input("1.Dig\n2.Flag\n")
        r = -1
        c = -1
        if mode == str(1):
            print("Digging mode ⛏️")
            r, c = input("Enter coordinates to dig as (r, c): ").split(' ')
        else:
            print("Flagging mode 🚩")
            r, c = input("Enter coordinates to flag as (r, c): ").split(' ')
        r = int(r)
        c = int(c)
        if not board.make_move(r, c, mode):
            print(board)
            print(f"{TextColor.RED}You lost :({TextColor.RESET}")
            return
        # print(f"vis size: {len(board.vis)}")
        # print(f"flag size: {len(board.flag)}")
        print(board)
    # print(board.bombs)
    if set(board.bombs) == board.flag:
        print("Hurray!!! You won")


while True:
    size = 5
    board = Board(size)
    # for bomb in board.bombs:
    #     x = bomb // size
    #     y = bomb % size
    #     print(f"x: {x}, y: {y}")
    play_minesweeper(board)
    ch = input("Try Again? (y/n): ")
    if ch.lower() == 'n':
        print("Exiting...")
        break