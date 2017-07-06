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

    def board_to_string(self):  # will be used for client server communication
        ret_str = ''
        for i in range(0, 9):
            for j in range(0, 9):
                ret_str += str(self.board[i][j]) + " "
            ret_str += '\n'
        return ret_str

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
        print(self.board_to_string())
        print('CURRENT PLAYER')
        print(self.current_player)
        print('HISTORY')
        print(self.history)
        print('KO POINT')
        print(self.ko_point)
        print('CAPTURED BY WHITE')
        print(self.black_captured)
        print('CAPTURED BY BLACK')
        print(self.white_captured)

    def move(self, position):
        (status, message) = self.is_valid_move(position)
        if status:
            self.set_value(position, self.current_player)
            removed_stones = self.clean_hood(position)
            if removed_stones == 1:
                self.ko_point = position
            else:
                self.ko_point = None
            if self.current_player == black_stone:
                self.white_captured += removed_stones
            else:
                self.black_captured += removed_stones
            (x, y) = position
            self.history.append([x, y])
            self.change_player()
            return 'OK'
        return message

    def is_valid_move(self, position):
        if not is_valid_position(position):
            return False, 'Invalid position'
        if self.is_ko_move(position):
            return False, 'Ko Move'
        if self.get_value(position) != empty_stone:
            return False, 'Not empty stone'
        if self.is_move_suicidal(position):
            return False, 'Suicidal move'
        return True, 'OK'

    def is_ko_move(self, position):
        if self.ko_point is None:
            return False
        (x, y) = position
        (ko_x, ko_y) = self.ko_point
        return ko_x == x and ko_y == y

    def is_move_suicidal(self, position):
        self.set_value(position, self.current_player)
        group = self.create_group(position)
        if not self.has_group_liberties(group):
            self.set_value(position, empty_stone)
            return True
        self.set_value(position, empty_stone)
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
        white_score += 6.5
        return 1 if black_score > white_score else -1

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

    def clean_hood(self, position):
        stones_removed = 0
        neighbors = get_normal_neighbors(position)
        for neighbor in neighbors:
            group = self.create_group(neighbor)
            if not self.has_group_liberties(group):
                stones_removed += self.remove_group(group)
        return stones_removed

    def board_to_list(self):
        return self.board.tolist()

    def clone_board_state(self):
        board2 = BoardState()
        board2.board = np.empty_like(self.board)
        board2.board[:] = self.board
        board2.current_player = self.current_player
        board2.ko_point = self.ko_point
        board2.history = self.history[:]
        board2.black_captured = self.black_captured
        board2.white_captured = self.white_captured
        return board2

    def get_all_possible_moves(self):
        moves = []
        for i in range(0, 9):
            for j in range(0, 9):
                status, _ = self.is_valid_move((i, j))
                if status:
                    moves.append((i, j))
        return moves

    @staticmethod
    def clear_board():
        board2 = BoardState()
        return board2
