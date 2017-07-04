from board import BoardState


def main():
    board_state = BoardState()
    board_state.move((0, 0))
    board_state.move((0, 1))
    board_state.move((8, 8))
    board_state.move((1, 0))
    board_state.print_state()

main()
