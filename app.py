from decouple import config
from flask import Flask, request


DEBUG = config('DEBUG', False, cast=bool)


app = Flask(__name__)


@app.route('/postreceive', methods=['POST'])
def postreceive():
    print("FORM:")
    print(dict(request.form))
    print("BODY:")
    try:
        print(request.get_json())
    except AttributeError:
        print('*no body*')
    return "OK"


@app.route('/')
def homepage():
    return "See README\n"


if __name__ == '__main__':
    app.run(debug=DEBUG, use_reloader=DEBUG)
