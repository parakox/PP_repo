from flask import Flask
app = Flask(__name__)

DATABASE = 'db/database.db'

@app.route('/api/v1/hello-world-28', methods = ['GET'])
def hello():
    return "Hello World 28"

if __name__ == '__main__':
    app.run()
