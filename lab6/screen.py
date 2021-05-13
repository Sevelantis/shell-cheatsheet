"""
thread module to quit program to print stuff on the Screen
"""

# imports
from threading import Thread
import time
import curses
import random as rand

class Displayer():
    """Displayer module enables to print nice strings in place on the screen"""
    def __init__(self):
        """Displayer constructor"""
        self.init_curses()

    def init_curses(self):
        """initializes screen"""
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.echo()
        curses.cbreak()
        self.stdscr.keypad(True)

    def quit_curses(self):
        """quits curses, sets settings back to default"""
        curses.echo()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()

    def clear(self):
        """clears screen"""
        self.stdscr.clear()

    def refresh(self):
        """refresh screen"""
        self.stdscr.refresh()

    def getch(self):
        """gets single key press"""
        return self.stdscr.getch()

    def print(self, row, col, text, color=1, mode=curses.A_NORMAL):
        """print to the screen with effects to position XY"""
        self.stdscr.addstr(row, col, text, curses.color_pair(color) | mode)

    def get_window_size(self):
        """gets terminal size letter rows and cols"""
        return self.stdscr.getmaxyx()

class GameBoard():
    """board module, AI enemy ( you aint gonna win )"""

    def __init__(self):
        """GameBoard constructor"""
        self.game_counter = 0
        self.is_player = True # player is a circle
        self.is_any_move = True
        self.points_player = 0
        self.points_enemy = 0
        self.winner = '-'
        self.moves_enemy = []
        self.rows = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]
        self.cols = [
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8]
        ]
        self.diagonals = [
            [2, 4, 6],
            [0, 4, 8]
        ]
        self.new_game()

    def get_decision_enemy(self):
        """computer AI - decides best for current situation"""
        choice = -1
        moves_total = self.get_moves_total()
        corners = [0, 2, 6, 8]
        if moves_total == 0:
            # take any corner
            choice = corners[rand.randint(0, 3)]
            self.moves_enemy.append(choice)
        elif moves_total == 1:
            # try center
            center = 4
            if self.is_move_legal(center):
                choice = center
            # get any corner
            else:
                choice = self.get_free_corner()
            self.moves_enemy.append(choice)
        elif moves_total == 2:
            # try opposite corner
            opposite_corner = self.get_opposite_corner(self.moves_enemy[0])
            if self.is_move_legal(opposite_corner):
                choice = opposite_corner
            # else take any free corner
            else:
                choice = self.get_free_corner()
            self.moves_enemy.append(choice)
        elif moves_total == 3:
            # if 2 'X' in a line, go there
            # else if 2 'O' in a line, go there
            # else go to corner
            space_in_line = self.get_space_in_line()
            if space_in_line != -1 and self.is_move_legal(space_in_line):
                choice = space_in_line
            else:
                if self.is_corner_attack():
                    choice = self.get_defensive_corner()
                else:
                    choice = self.get_free_middle()
            self.moves_enemy.append(choice)
        elif moves_total == 4 or moves_total == 6:
            # if 2 'X' in a line, go there
            # else if 2 'O' in a line, go there
            # else go to corner
            space_in_line = self.get_space_in_line()
            if space_in_line != -1 and self.is_move_legal(space_in_line):
                choice = space_in_line
            else:
                choice = self.get_free_corner()
            self.moves_enemy.append(choice)
        elif moves_total == 8:
            # go to free space
            free_space = self.moves.index(' ')
            choice = free_space
            self.moves_enemy.append(choice)
        else:
            # if 2 'X' in a line, go there
            # else if 2 'O' in a line, go there
            # else go to corner
            space_in_line = self.get_space_in_line()
            if space_in_line != -1 and self.is_move_legal(space_in_line):
                choice = space_in_line
            else:
                choice = self.get_free_corner()
            self.moves_enemy.append(choice)
        return choice

    def is_corner_attack(self):
        return [self.moves[i] for i in [1, 3, 5, 7]].count('O') == 2

    def get_defensive_corner(self):
        middles = [1, 3, 5, 7]
        middle_pairs = [
            [1, 5, 2],
            [1, 3, 0],
            [3, 7, 6],
            [5, 7, 8]
        ]
        for pair in middle_pairs:
            if self.moves[pair[0]] == 'O' and self.moves[pair[1]] == 'O':
                return pair[2]

    def get_space_in_line(self):
        """returns best move if a line with a space exists"""
        marks = ['X', 'O']

        choices = []
        choice = -1
        for mark in marks:
            for row in self.rows:
                choice = self.get_idx_in_row(row, mark)
                if choice != -1:
                    choices.append((choice, mark))
            for col in self.cols:
                choice = self.get_idx_in_row(col, mark)
                if choice != -1:
                    choices.append((choice, mark))
            for diagonal in self.diagonals:
                choice = self.get_idx_in_row(diagonal, mark)
                if choice != -1:
                    choices.append((choice, mark))
        if choices:
            # check winning move
            for point in choices:
                if point[1] == self.get_current_player_mark():
                    return point[0]
            # defensive move
            return choices[rand.randint(0, len(choices)-1)][0]
        return -1

    def get_idx_in_row(self, row, mark):
        """given a row / col / diagonal, returns index of free place"""
        cnt_mark = 0
        cnt_free = 0
        idx_free = -1
        for i in row:
            if self.moves[i] == mark:
                cnt_mark += 1
            elif self.moves[i] == ' ':
                cnt_free += 1
        if cnt_mark == 2 and cnt_free == 1:
            for i in row:
                if self.moves[i] == ' ':
                    idx_free = i
        return idx_free

    def get_free_corner(self):
        """gets free corrner"""
        corners = [0, 2, 6, 8]
        legal = []
        for corner in corners:
            if self.is_move_legal(corner):
                legal.append(corner)
        if legal:
            return legal[rand.randint(0, len(legal)-1)]
        return -1

    def get_free_middle(self):
        """gets free middle"""
        middles = [1, 3, 5, 7]
        legal = []
        for middle in middles:
            if self.is_move_legal(middle):
                legal.append(middle)
        if legal:
            return legal[rand.randint(0, len(legal)-1)]
        return -1

    @classmethod
    def get_opposite_corner(cls, idx):
        """return opposite corner of given one"""
        if idx == 0:
            return 8
        if idx == 8:
            return 0
        if idx == 6:
            return 2
        if idx == 2:
            return 6
        return -1

    def make_move(self, idx):
        """handles idx action - keyboard or AI enemy decision"""
        if self.is_move_legal(idx) and self.is_any_move:
            self.legal_move(idx)
            self.update_winner()
        else:
            self.illegal_move()

    def update_winner(self):
        """checks win combinations"""
        if ' ' not in self.moves:
            self.is_any_move = False
            return
        # check if there is a winner, if there is, set winner
        marks = ['O', 'X']
        for mark in marks:
            # horizontal 3 in a line
            is_winner = False
            for row in self.rows:
                if [self.moves[i] for i in row].count(mark) == 3:
                    is_winner = True
            # vertical 3 in a line
            for col in self.cols:
                if [self.moves[i] for i in col].count(mark) == 3:
                    is_winner = True
            # diagonal 3 in a line
            for diagonal in self.diagonals:
                if [self.moves[i] for i in diagonal].count(mark) == 3:
                    is_winner = True

            if is_winner:
                self.winner = mark
                self.is_any_move = False
                if self.winner == 'X':
                    self.points_enemy += 1
                elif self.winner == 'O':
                    self.points_player += 1

    def is_move_legal(self, idx):
        """checks if move is legal"""
        if idx == -1:
            return False
        return self.moves[idx] == ' '

    def get_current_player_mark(self):
        """gets current mark"""
        if self.is_player:
            return 'O'
        return 'X'

    def get_current_player_name(self):
        """get current player name :)"""
        if self.is_player:
            return 'PLAYER'
        return 'ENEMY COMPUTER'

    def get_moves_total(self):
        """returns total number of moves made in current game"""
        return self.moves.count('X') + self.moves.count('O')

    def legal_move(self, idx):
        """executes legal move- sets mark on proper place, adds move, switches player"""
        self.moves[idx] = self.get_current_player_mark()
        idx_xy = self.values_xy[idx]
        self.board[idx_xy[0]][idx_xy[1]] = self.get_current_player_mark()
        self.is_player = not self.is_player

    @classmethod
    def illegal_move(cls):
        """prints illegal move info"""
        info = "MOVE NOT LEGAL!"
        info_len = len(info)
        point = DISPLAYER.get_window_size()
        for i in range(0, int(point[0])):
            for j in range(0, point[1]-info_len, info_len):
                DISPLAYER.print(i, j, info, color=2, mode=curses.A_BOLD | curses.A_ITALIC)

    def print_board(self):
        """prints: board, controls, info to the screen"""
        rows = len(self.board)
        cols = len(self.board[0])

        offset_rows = 1
        offset_cols = 5
        distance_boards = 35
        for col in range(cols):
            for row in range(rows):
                DISPLAYER.print(row+offset_rows, col+offset_cols, str(self.board[row][col]), mode=curses.A_BOLD)
                DISPLAYER.print(row+offset_rows, col+offset_cols+distance_boards, str(self.board_helper[row][col]), 3)
        cols_info = distance_boards
        rows_info = 0
        DISPLAYER.print(rows_info, cols_info+2, '**C.O.N.T.R.O.L.S.**', color=3, mode=curses.A_BLINK)
        DISPLAYER.print(rows_info+9, cols_info+2, '\'r\' - RESET / NEW GAME!!', color=3,)
        DISPLAYER.print(rows_info+11, cols_info+2, '\'q\' - QUIT :\'(', color=3)
        DISPLAYER.print(rows_info+9, offset_cols, f"'{self.get_current_player_name()}' MOVES!", color=3, mode=curses.A_BOLD)
        DISPLAYER.print(rows_info+13, offset_cols, f"YOUR wins: {self.points_player}, ENEMY wins: {self.points_enemy}", color=3, mode=curses.A_BOLD)

        if not self.is_any_move:
            if self.winner == '-':
                DISPLAYER.print(11, 5, f"GAME ENDED! winner: NOBODY!!", color=3, mode=curses.A_BOLD|curses.A_BLINK)
            else:
                DISPLAYER.print(11, 5, f"GAME ENDED! WINNER: '{self.winner}'", color=2, mode=curses.A_BOLD|curses.A_BLINK)
        else:
            DISPLAYER.print(11, 5, f"GAME IN PROGRES...", color=3, mode=curses.A_BOLD)

    def new_game(self):
        """resets settings for new game"""
        if self.game_counter % 2 == 1:
            self.is_player = False
        self.is_any_move = True
        self.game_counter += 1

        self.moves_enemy = []
        # self.is_player = False

        self.board = [
            ['+', '-', '-', '-', '+', '-', '-', '-', '+', '-', '-', '-', '+'],
            ['|', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|'],
            ['+', '-', '-', '-', '+', '-', '-', '-', '+', '-', '-', '-', '+'],
            ['|', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|'],
            ['+', '-', '-', '-', '+', '-', '-', '-', '+', '-', '-', '-', '+'],
            ['|', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|'],
            ['+', '-', '-', '-', '+', '-', '-', '-', '+', '-', '-', '-', '+']
        ]
        self.board_helper = [
            ['+', '-', '-', '-', '+', '-', '-', '-', '+', '-', '-', '-', '+'],
            ['|', ' ', '1', ' ', '|', ' ', '2', ' ', '|', ' ', '3', ' ', '|'],
            ['+', '-', '-', '-', '+', '-', '-', '-', '+', '-', '-', '-', '+'],
            ['|', ' ', '4', ' ', '|', ' ', '5', ' ', '|', ' ', '6', ' ', '|'],
            ['+', '-', '-', '-', '+', '-', '-', '-', '+', '-', '-', '-', '+'],
            ['|', ' ', '7', ' ', '|', ' ', '8', ' ', '|', ' ', '9', ' ', '|'],
            ['+', '-', '-', '-', '+', '-', '-', '-', '+', '-', '-', '-', '+']
        ]
        self.values_xy = [
            (1, 2), (1, 6), (1, 10),
            (3, 2), (3, 6), (3, 10),
            (5, 2), (5, 6), (5, 10)
        ]
        self.moves = [
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
        ]

class Screen(Thread):
    """runs 2 threads, Screen and read keyboard to handle curses game"""

    def __init__(self):
        """Screen constructor"""
        self.running = True
        self.board = GameBoard()
        # Screen thread
        Thread.__init__(self)
        # keyboard thread
        self.keyboard_thread = Thread(target=self.read_keyboard, args=())
        self.keyboard_thread.start()

    def read_keyboard(self):
        """thread to read keyboard idx"""
        keys = [
            ord('1'), ord('2'), ord('3'),
            ord('4'), ord('5'), ord('6'),
            ord('7'), ord('8'), ord('9')
        ]
        while True:
            if self.board.is_any_move:
                if self.board.is_player:        # player move
                    getch = DISPLAYER.getch()
                    if getch == ord('q'):       # quit game on 'q' press
                        break
                    if getch == ord('r'):     # reset board on 'r' press
                        self.board.new_game()
                    if getch in keys:
                        self.board.make_move(idx=keys.index(getch))
                else:                           # computer enemy automatic move
                    time.sleep(rand.uniform(0.2, 0.5))
                    self.board.make_move(idx=self.board.get_decision_enemy())

        self.running = False

    def run(self):
        """
        update Screen
        """
        while self.running:
            self.update_screen()

            if not self.board.is_any_move:
                self.update_screen()
                self.board.new_game()
                time.sleep(2)
            time.sleep(.5)
        DISPLAYER.quit_curses()
        self.keyboard_thread.join()
    def update_screen(self):
        """clears, sets image, displays image"""
        DISPLAYER.clear()
        self.board.print_board()
        DISPLAYER.refresh()
DISPLAYER = Displayer()
