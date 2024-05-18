from flask import Flask
from auth import auth


app = Flask(__name__)

app.register_blueprint(auth, url_prefix='/auth')


if __name__ == '__main__':
    app.run(debug=True)
