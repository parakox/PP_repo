from flask import Flask
app = Flask(__name__)


@app.route('/api/v1/hello-world-28')
def hello():
    print("1")
    return "Hello World 28"

if __name__ == '__main__':
    app.run()