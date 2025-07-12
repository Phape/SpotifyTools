from flask import Flask
from flask_assets import Bundle, Environment
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sass_embedded import compile_file

from . import settings

app = Flask(__name__)
app.config.from_object(settings)

assets = Environment(app)
assets.url = app.static_url_path

# Import and register custom Dart Sass filter

# Compile SCSS file
css = compile_file("app/static/css/main.scss", dest="app/static/css/main.css") # todo maybe deactivate source map generation in prod
css_bundle = Bundle("css/main.scss")
assets.register("scss_all", css_bundle)

Session(app)

# Import routes after app initialization to avoid circular imports
from . import routes  # noqa: E402
