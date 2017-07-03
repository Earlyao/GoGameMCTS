from board import BoardState


def main():
    board = BoardState()
    board.print_state()
    print(board.move((1, 1)))
    board.print_state()
    print(board.move((1, 2)))
    print(board.move((8, 8)))
    board.print_state()
    print('NIJE')
    print(board.is_end_of_game())
    board.pass_move()
    print(board.is_end_of_game())
    board.pass_move()
    print('JESTE')
    print(board.is_end_of_game())
    print(board.get_winner())

main()
