from board import BoardState


def main():
    board_state = BoardState()
    board_state.test_method()
    board_state.print_board()
    grupica = board_state.create_group((2, 2))
    print(grupica)
    br = board_state.remove_group(grupica)
    board_state.print_board()
    print(br)

main()
