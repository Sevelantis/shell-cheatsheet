# Podstawowe Podstawy Programowania w Pythonie
"""
module circle and cross console game
"""

# imports
from screen import Screen

if __name__ == '__main__':
    SCR_THREAD = Screen()
    SCR_THREAD.start()
    # wait till thread finishes
    SCR_THREAD.join()
