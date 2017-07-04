import numpy as np


empty_stone = 0
black_stone = 1
white_stone = -1


def is_valid_position(position):
    (x, y) = position
    return 0 <= x < 9 and 0 <= y < 9


def get_normal_neighbors(position):
    (x, y) = position
    ret_val = []
    if is_valid_position((x+1, y)):
        ret_val.append((x+1, y))
    if is_valid_position((x-1, y)):
        ret_val.append((x-1, y))
    if is_valid_position((x, y+1)):
        ret_val.append((x, y+1))
    if is_valid_position((x, y-1)):
        ret_val.append((x, y-1))
    return ret_val


class BoardState(object):
    def __init__(self):
        self.board = np.zeros((9, 9))
        self.current_player = black_stone
        self.ko_point = None
        self.history = []
        self.black_captured = 0  # number of captures made by white
        self.white_captured = 0  # number of captures made by black

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
        print('HISTORY')
        print(self.history)
        # print('KO POINT')
        # print(self.ko_point)

    def move(self, position):
        if self.is_valid_move(position):
            self.set_value(position, self.current_player)
            (x, y) = position
            self.history.append([x, y])
            self.change_player()
            return True
        return False

    def is_valid_move(self, position):
        if not is_valid_position(position):
            return False
        if self.is_ko_move(position):
            return False
        if self.get_value(position) != empty_stone:
            return False
        if self.is_move_suicidal(position):
            return False
        return True

    def is_ko_move(self, position):
        if self.ko_point is None:
            return False
        (x, y) = position
        (ko_x, ko_y) = self.ko_point
        return ko_x == x and ko_y == y

    def is_move_suicidal(self, position):
        return False

    def pass_move(self):
        self.history.append([100, 100])
        self.ko_point = None
        self.change_player()

    def is_end_of_game(self):
        if len(self.history) > 2:
            if self.history[-1] == [100, 100] and self.history[-2] == [100, 100]:
                return True
        return False

    def get_winner(self):
        black_score = (self.board > 0).sum()
        white_score = (self.board < 0).sum()
        black_score += self.white_captured
        white_score += self.black_captured
        return black_score, white_score

    def create_group(self, position, group=None):
        if group is None:
            group = {position}
        color = self.get_value(position)
        neighbors = get_normal_neighbors(position)
        for neighbor in neighbors:
            if neighbor not in group:
                if self.get_value(neighbor) == color:
                    group.add(neighbor)
                    ret_val = self.create_group(neighbor, group)
                    for temp_position in ret_val:
                        group.add(temp_position)
        return group

    def has_group_liberties(self, group):
        for position in group:
            current_neighbors = get_normal_neighbors(position)
            for neighbor in current_neighbors:
                if self.get_value(neighbor) == empty_stone:
                    return True
        return False

    def remove_group(self, group):
        stones_removed = 0
        for position in group:
            self.set_value(position, empty_stone)
            stones_removed += 1
        return stones_removed

    def test_method(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if i == 2:
                    self.board[i, j] = black_stone
                if j == 2:
                    self.board[i, j] = white_stone
        self.board[0, 1] = 1
        self.board[1, 0] = 1

