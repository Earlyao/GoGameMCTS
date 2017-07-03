from board import BoardState


def main():
    board = BoardState()
    board.print_state()
    print(board.move((1, 1)))
    board.print_state()
    print(board.move((1, 1)))
    print(board.move((8, 8)))
    board.print_state()


main()
