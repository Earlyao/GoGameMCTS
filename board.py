import numpy as np


empty_stone = 0
black_stone = 1
white_stone = -1


def is_valid_position(position):
    (x, y) = position
    return 0 <= x < 9 and 0 <= y < 9


class BoardState(object):
    def __init__(self):
        self.board = np.zeros((9, 9))
        self.current_player = black_stone
        self.black_passed = False
        self.white_passed = False
        self.ko_point = None

    def print_board(self):  # will be used for client server communication
        for i in range(0, 9):
            for j in range(0, 9):
                print(self.board[i][j], end=" ")
            print()

    def change_player(self):
        self.current_player = - self.current_player

    def get_value(self, position):
        (x, y) = position
        return self.board[x, y]

    def set_value(self, position, color):
        (x, y) = position
        self.board[x, y] = color

    """Debugging method"""
    def print_state(self):
        print('BOARD:')
        self.print_board()
        print('CURRENT PLAYER')
        print(self.current_player)
        # print('PASSES')
        # print(self.black_passed, self.white_passed)
        # print('KO POINT')
        # print(self.ko_point)

    def move(self, position):
        if self.is_valid_move(position):
            self.set_value(position, self.current_player)
            self.change_player()
            return True
        return False

    def is_valid_move(self, position):
        if not is_valid_position(position):
            return False
        if self.get_value(position) == empty_stone:
            return True
        return False
