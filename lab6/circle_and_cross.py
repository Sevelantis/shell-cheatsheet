# Podstawowe Podstawy Programowania w Pythonie
"""
module circle and cross console game
"""

# imports
from screen import *

if __name__ == '__main__':
    SCR_THREAD = screen()
    SCR_THREAD.start()
    # wait till thread finishes
    SCR_THREAD.join()
