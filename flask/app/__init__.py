import os

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

# Compile SCSS file
compile_file(
    os.path.join(app.static_folder, "css/main.scss"),
    dest=os.path.join(app.static_folder, "css/main.css"),
)  # todo maybe deactivate source map generation in prod
css_bundle = Bundle("css/main.css")
assets.register("scss_all", css_bundle)

Session(app)

# Import routes after app initialization to avoid circular imports
from . import routes  # noqa: E402
