from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Auto Accept Bot says HI'


if __name__ == "__main__":
    app.run()


