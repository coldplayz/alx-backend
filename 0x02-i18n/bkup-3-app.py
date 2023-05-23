#!/usr/bin/env python3
"""Basic Flask app.
"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext


class Config:
    """Configuration for the app.
    """
    LANGUAGES = ["en", "fr"]

    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


config = Config()

app = Flask(__name__)
app.config.from_object(config)
babel = Babel(app)


# define a locale selector
@babel.localeselector
def get_locale():
    """Selects the most appropriate locale to use per request.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/")
def index():
    """Index page.
    """
    # create message IDs, marked for translation
    title = gettext('home_title')
    header = gettext('home_header')

    return render_template('3-index.html', title, header)
