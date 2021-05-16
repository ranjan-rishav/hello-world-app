from flask import Flask

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def default():
        return "<p>Hello, World!</p>"
    return app