from flask import Flask, render_template
from board import BoardState


app = Flask(__name__)
result = BoardState()


@app.route('/')
def index():
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run()
