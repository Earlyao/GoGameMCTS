from flask import Flask, render_template, request, jsonify
from board import BoardState
from mtcs import MonteCarloTreeSearch

app = Flask(__name__)
board = BoardState()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/move', methods=['POST'])
def move():
    x = int(request.form['x'])
    y = int(request.form['y'])
    if x == 100 and y == 100:
        board.pass_move()
        board.pass_move()
        winner = board.get_winner()
        message = 'END OF GAME. '
        if winner == 1:
            message += 'BLACK PLAYER WINS'
        else:
            message += 'WHITE PLAYER WINS'

    else:
        message = board.move((y, x))
    if message == 'OK':
        bot = MonteCarloTreeSearch(board)
        result = bot.get_move(20)
        if result is not None:
            board.move(result.move)
        else:
            board.pass_move()
            message = 'PASS BY COMPUTER'
        if board.is_end_of_game():
            message = 'GAME OVER'
    return jsonify({'board': board.board_to_list(), 'message': message})

if __name__ == "__main__":
    app.run()
