#!venv/bin/python
from flask import Flask
from controllers.tasks_controller import tasks_api

app = Flask(__name__)

app.register_blueprint(tasks_api)


@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
