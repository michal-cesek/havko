from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    minute = datetime.now().minute
    return render_template('index.html', time=minute)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7648)
