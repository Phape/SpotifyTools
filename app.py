from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return f'If you can read this, everything is good.'

if __name__ == "__main__":
    app.run()