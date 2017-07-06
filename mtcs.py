import math
import random


class MTCSNode(object):
    def __init__(self, move, parent, color):
        self.move = move
        self.parent = parent
        self.children = []
        self.color = color
        self.wins = 0
        self.visits = 0

    def is_leaf(self):
        return self.children == []

    def is_root(self):
        return self.parent is None

    def expand(self, moves):
        i = 10
        while i > 0 and moves != []:
            new_move = random.choice(moves)
            self.children.append(MTCSNode(new_move, self, -self.color))
            moves.remove(new_move)
            i -= 1

    def ucb_value(self):
        if self.visits == 0:
            return float("inf")
        return self.wins/self.visits + math.sqrt(2) * math.sqrt(math.log(self.parent.visits)/self.visits)

    def update(self, result):
        self.wins += result
        self.visits += 1

    def update_recursive(self, result):
        if not self.is_root():
            self.parent.update_recursive(result)
        self.update(result)

    def select_best(self):
        if not self.children:
            return None
        max_value = self.children[0].ucb_value()
        ret_val = self.children[0]
        for child in self.children:
            if child.ucb_value() > max_value:
                max_value = child.ucb_value()
                ret_val = child
        return ret_val

    def most_wins_child(self):
        if not self.children:
            return None
        max_value = self.children[0].wins
        ret_val = self.children[0]
        for child in self.children:
            if child.wins < max_value:
                max_value = child.wins
                ret_val = child
        return ret_val


class MonteCarloTreeSearch(object):
    def __init__(self, board):
        self.board = board.clone_board_state()
        self.root = MTCSNode(board.history[-1], None, board.current_player)

    def selection(self):
        copy_board = self.board.clone_board_state()
        temp_node = self.root
        while not temp_node.is_leaf():
            copy_board.move(temp_node.move)
            temp_node = temp_node.select_best()
        return temp_node, copy_board

    @staticmethod
    def expansion(tree_node, board_state):
        if board_state.is_end_of_game():
            return False
        tree_node.expand(board_state.get_all_possible_moves())
        return True

    @staticmethod
    def simulation(tree_node, board_state):
        temp_node = tree_node.select_best()
        board_state.move(temp_node.move)
        while not board_state.is_end_of_game():
            moves = board_state.get_all_possible_moves()
            if len(moves) > 0:
                random_move = random.choice(moves)
                board_state.move(random_move)
            else:
                board_state.pass_move()
        result = board_state.get_winner()
        return result, temp_node

    @staticmethod
    def back_propagation(tree_node, result):
        result = -result
        tree_node.update_recursive(result)

    def get_move(self, number):
        while number > 0:
            tree_node, copy_board = self.selection()
            flag = self.expansion(tree_node, copy_board)
            if flag:
                result, tree_node = self.simulation(tree_node, copy_board)
                self.back_propagation(tree_node, result)
            else:
                self.back_propagation(tree_node, copy_board.get_winner())
            number -= 1
        return self.root.most_wins_child()
