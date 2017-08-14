from decouple import config
from flask import Flask, request


DEBUG = config('DEBUG', False, cast=bool)


app = Flask(__name__)


@app.route('/postreceive', methods=['POST', 'GET'])
def postreceive():
    if request.method == 'GET':
        return "Yeah, it works but use POST\n"
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
