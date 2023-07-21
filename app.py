from flask import Flask
import test.py

app = Flask(__name__)

@app.route('/')
def hello():
    return 'IPS & MUSKAN'

if __name__ == '__main__':
    app.run()

