from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World 1!'

def create_app():
    return
if __name__ == '__main__':
    app.run(debug=True)
