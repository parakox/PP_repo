from flask import Flask
app = Flask(__name__)


@app.route('/api/v1/hello-world-28')
def hello():
    return "Hello World 28"

if __name__ == '__main__':
    app.run()