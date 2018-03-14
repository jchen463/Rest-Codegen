#!venv/bin/python
from flask import Flask
from controllers.tasks_controller import tasks_api
from controllers.default_controller import default_api
import encoder


def main():
    app = Flask(__name__)
    app.json_encoder = encoder.JSONEncoder
    # app.json_decoder
    app.register_blueprint(tasks_api)
    app.register_blueprint(default_api)
    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
