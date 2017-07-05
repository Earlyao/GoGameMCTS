from flask import Flask, render_template, request, jsonify
from board import BoardState


app = Flask(__name__)
board = BoardState()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/move', methods=['POST'])
def move():
    x = int(request.form['x'])
    y = int(request.form['y'])
    print((x, y))
    message = board.move((y, x))
    board.print_state()
    return jsonify({'board': board.board_to_list(), 'message': message})

if __name__ == "__main__":
    app.run()
