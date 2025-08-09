# init.py
from flask import Flask
from flasgger import Swagger
from app.routes.pdf_in import upload_bp  # импортируем блюпринт из pdf_in.py
from .db import init_db

def create_app():
    apps = Flask(__name__)

    Swagger(apps)  # Swagger UI будет по /apidocs

    apps.register_blueprint(upload_bp, url_prefix='/resume')

    init_db()

    @apps.get("/")
    def hello_world():
        return "Hello, World!"

    return apps


if __name__ == "__main__":
    application = create_app()
    application.run(host="127.0.0.1", port=5001, debug=True)
