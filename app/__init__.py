from pathlib import Path

from flask import Flask

from app.config import Config
from app.routes import main


def create_app():
    base_dir = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static"),
    )

    app.config.from_object(Config)
    app.register_blueprint(main)

    return app