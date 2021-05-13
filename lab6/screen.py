"""
thread module to quit program to print stuff on the screen
"""

# imports
import os
import threading
from threading import Thread
import time
import curses
import random as rand
import subprocess

class displayer():
    def __init__(self):
        self.init_curses()

    def init_curses(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.echo()
        curses.cbreak()
        self.stdscr.keypad(True)

    def quit_curses(self):
        curses.echo()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()

    def clear(self):
        self.stdscr.clear()
    
    def refresh(self):
        self.stdscr.refresh()

    def getch(self):
        return self.stdscr.getch() 
    
    def print(self, x, y, str, color=1, type=curses.A_NORMAL):
        self.stdscr.addstr(x, y, str, curses.color_pair(color) | type)
    
    def get_window_size(self):
        return self.stdscr.getmaxyx()

class game_board():

    def __init__(self):
        self.game_counter = 0
        self.is_player = True # player is a circle
        self.is_any_move = True
        self.points_player = 0
        self.points_enemy = 0
        self.winner = '-'
        self.moves_enemy = []
        self.new_game()

    def get_decision_enemy(self):
        choice = -1
        moves_total = self.get_moves_total()
        corners = [0,2,6,8]
        if moves_total == 0:
            # take any corner
            choice = corners[rand.randint(0,3)]
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
            

    def get_space_in_line(self):
        marks = ['X', 'O']
        rows = [
            [0,1,2],
            [3,4,5],
            [6,7,8]
        ]
        cols = [
            [0,3,6],
            [1,4,7],
            [2,5,8]
        ]
        diagonals = [
            [2,4,6],
            [0,4,8]
        ]

        choices = []
        choice = -1
        for mark in marks:
            for row in rows:
                choice = self.get_idx_in_row(row, mark)
                if choice != -1:
                    choices.append((choice, mark))
            for col in cols:
                choice = self.get_idx_in_row(col, mark)
                if choice != -1:
                    choices.append((choice, mark))
            for diagonal in diagonals:
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
        else:
            return -1

    def get_idx_in_row(self, row, mark):
        cnt_mark = 0
        cnt_free = 0
        idx_free =-1
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
        corners = [0,2,6,8]
        legal = []
        for corner in corners:
            if self.is_move_legal(corner):
                legal.append(corner)
        if legal:
            return legal[rand.randint(0,len(legal)-1)]
        return -1

    def get_free_middle(self):
        middles = [1,3,5,7]
        legal = []
        for middle in middles:
            if self.is_move_legal(middle):
                legal.append(middle)
        if legal:
            return legal[rand.randint(0,len(legal)-1)]
        return -1

    def get_opposite_corner(self, input):
        if input == 0:
            return 8
        elif input == 8:
            return 0
        elif input == 6:
            return 2
        elif input == 2:
            return 6

    def make_move(self, input):
        if self.is_move_legal(input) and self.is_any_move:
            self.legal_move(input)
            self.update_winner()
        else:
            self.illegal_move()

    def update_winner(self):
        if ' ' not in self.moves:
            self.is_any_move = False
            return
        # check if there is a winner, if there is, set winner
        pos = self.moves
        marks = ['O', 'X']
        for i in range(2):
            # horizontal 3 in a row
            # vertical 3 in a ro\w
            # oblique 3 in a row
            if (pos[0] == marks[i] and pos[1] == marks[i] and pos[2] == marks[i]) or \
                (pos[3] == marks[i] and pos[4] == marks[i] and pos[5] == marks[i]) or \
                (pos[6] == marks[i] and pos[7] == marks[i] and pos[8] == marks[i]) or \
                (pos[0] == marks[i] and pos[3] == marks[i] and pos[6] == marks[i]) or \
                (pos[1] == marks[i] and pos[4] == marks[i] and pos[7] == marks[i]) or \
                (pos[2] == marks[i] and pos[5] == marks[i] and pos[8] == marks[i]) or \
                (pos[0] == marks[i] and pos[4] == marks[i] and pos[8] == marks[i]) or \
                (pos[2] == marks[i] and pos[4] == marks[i] and pos[6] == marks[i]):
                    self.winner = marks[i]
                    self.is_any_move = False
                    if self.winner == 'X':
                        self.points_enemy+=1
                    elif self.winner == 'O':
                        self.points_player+=1


    def is_move_legal(self, input):
        if input == -1:
            return False
        return self.moves[input] == ' '

    def get_current_player_mark(self):
        if self.is_player:
            return 'O'
        else:
            return 'X'
            
    def get_current_player_name(self):
        if self.is_player:
            return 'PLAYER'
        else:
            return 'ENEMY COMPUTER'
    
    def get_moves_total(self):
        return self.moves.count('X') + self.moves.count('O')

    def legal_move(self, input):
        self.moves[input] = self.get_current_player_mark()
        input_xy = self.values_xy[input]
        self.board[input_xy[0]][input_xy[1]] = self.get_current_player_mark()
        self.is_player = not self.is_player

    def illegal_move(self):
        info = "MOVE NOT LEGAL!"
        info_len = len(info)
        point = displayer.get_window_size()
        for i in range(0, int(point[0])):
            for j in range(0, point[1]-info_len, info_len):
                displayer.print(i, j, info, color=2, type=curses.A_BOLD | curses.A_ITALIC)

    def print_board(self):
        rows = len(self.board)
        cols = len(self.board[0])
        
        offset_rows = 1
        offset_cols = 5
        distance_boards = 35
        for y in range(cols):
            for x in range(rows):
                displayer.print(x+offset_rows, y+offset_cols, str(self.board[x][y]), type=curses.A_BOLD)
                displayer.print(x+offset_rows, y+offset_cols+distance_boards, str(self.board_helper[x][y]), 3)
        cols_info = distance_boards
        rows_info = 0
        displayer.print(rows_info, cols_info+2, '**C.O.N.T.R.O.L.S.**', color=3,type=curses.A_BLINK)
        displayer.print(rows_info+9, cols_info+2, '\'r\' - RESET / NEW GAME!!', color=3,)
        displayer.print(rows_info+11, cols_info+2, '\'q\' - QUIT :\'(', color=3,)
        displayer.print(rows_info+9, offset_cols, f"'{self.get_current_player_name()}' MOVES!", color=3, type=curses.A_BOLD)
        displayer.print(rows_info+13, offset_cols, f"YOUR wins: {self.points_player}, ENEMY wins: {self.points_enemy}", color=3, type=curses.A_BOLD)
        
        if not self.is_any_move:
            if self.winner == '-':
                displayer.print(11, 5, f"GAME ENDED! winner: NOBODY!!", color=3, type=curses.A_BOLD|curses.A_BLINK)
            else:
                displayer.print(11, 5, f"GAME ENDED! WINNER: '{self.winner}'", color=2, type=curses.A_BOLD|curses.A_BLINK)
        else:
            displayer.print(11, 5, f"GAME IN PROGRES...", color=3, type=curses.A_BOLD)

    def new_game(self):
        if self.game_counter % 2 == 1:
            self.is_player = False
        self.is_any_move = True
        self.game_counter += 1

        self.moves_enemy = []
        # self.is_player = False

        self.board = [
            ['+','-','-','-','+','-','-','-','+','-','-','-','+'],
            ['|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|'],
            ['+','-','-','-','+','-','-','-','+','-','-','-','+'],
            ['|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|'],
            ['+','-','-','-','+','-','-','-','+','-','-','-','+'],
            ['|',' ',' ',' ','|',' ',' ',' ','|',' ',' ',' ','|'],
            ['+','-','-','-','+','-','-','-','+','-','-','-','+']
        ]
        self.board_helper = [
            ['+','-','-','-','+','-','-','-','+','-','-','-','+'],
            ['|',' ','1',' ','|',' ','2',' ','|',' ','3',' ','|'],
            ['+','-','-','-','+','-','-','-','+','-','-','-','+'],
            ['|',' ','4',' ','|',' ','5',' ','|',' ','6',' ','|'],
            ['+','-','-','-','+','-','-','-','+','-','-','-','+'],
            ['|',' ','7',' ','|',' ','8',' ','|',' ','9',' ','|'],
            ['+','-','-','-','+','-','-','-','+','-','-','-','+']
        ]
        self.values_xy=[
            (1,2), (1,6), (1,10),
            (3,2), (3,6), (3,10),
            (5,2), (5,6), (5,10)
        ]
        self.moves=[
            ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
        ]

class screen(Thread):

    def __init__(self):
        self.running=True
        self.board = game_board()
        # screen thread
        Thread.__init__(self)
        # keyboard thread
        self.keyboard_thread=Thread(target=self.read_keyboard, args=())
        self.keyboard_thread.start()
    
    def read_keyboard(self):
        keys = [
            ord('1'),ord('2'),ord('3'),
            ord('4'),ord('5'),ord('6'),
            ord('7'),ord('8'),ord('9')
        ]
        while True:
            if self.board.is_any_move:
                if self.board.is_player:        # player move
                    getch = displayer.getch()
                    if getch == ord('q'):       # quit game on 'q' press
                        break
                    elif getch == ord('r'):     # reset board on 'r' press
                        self.board.new_game()
                    elif getch in keys:
                        self.board.make_move(input=keys.index(getch))
                else:                           # computer enemy automatic move
                    time.sleep(rand.uniform(0.2, 0.5))
                    self.board.make_move(input=self.board.get_decision_enemy())

        self.running=False

    def run(self):
        """
        update screen
        """
        while self.running:
            self.update_screen()

            if not self.board.is_any_move:
                self.update_screen()
                self.board.new_game()
                time.sleep(2)
            time.sleep(.5)

        displayer.quit_curses()
        self.keyboard_thread.join()

    def update_screen(self):
        displayer.clear()
        self.board.print_board()
        space = self.board.get_space_in_line()
        displayer.refresh()

displayer = displayer()