from flask import Flask
from repo import repo

from dotenv import load_dotenv

app = Flask(__name__)
app.register_blueprint(repo)


@app.route('/')
def index():
    return ""


if __name__ == '__main__':
    load_dotenv()
    app.run()
