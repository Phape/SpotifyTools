from flask import Flask
from flask_assets import Bundle, Environment
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from .sass_filter import DartSassFilter

from . import settings

app = Flask(__name__)
app.config.from_object(settings)

assets = Environment(app)
assets.url = app.static_url_path

# Register custom Dart Sass filter
assets.register('dartsass', DartSassFilter)

# Create SCSS bundle with Dart Sass
scss = Bundle("css/main.scss", filters="dartsass", output="css/main.css")
assets.register("scss_all", scss)

Session(app)

# Import routes after app initialization to avoid circular imports
from . import routes  # noqa: E402
