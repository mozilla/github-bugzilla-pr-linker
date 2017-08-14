from flask import Flask
app = Flask(__name__)


@app.route('/')
def homepage():
    return "See README\n"


if __name__ == '__main__':
    # XXX env DEBUG instead
    app.run(debug=True, use_reloader=True)
