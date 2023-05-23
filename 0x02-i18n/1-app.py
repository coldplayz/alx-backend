#!/usr/bin/env python3
"""Basic Flask app.
"""
from flask import Flask, render_template
from flask_babel import Babel


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


@app.route("/")
def index():
    """Index page.
    """
    return render_template('0-index.html')
