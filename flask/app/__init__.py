from flask import Flask
from flask_assets import Bundle, Environment
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from . import settings

app = Flask(__name__)
app.config.from_object(settings)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle("css/main.scss", filters="libsass", output="css/main.css")
assets.register("scss_all", scss)

Session(app)

# Import routes after app initialization to avoid circular imports
from . import routes  # noqa: E402
