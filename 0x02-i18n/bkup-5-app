#!/usr/bin/env python3
"""Basic Flask app.
"""
from flask import Flask, render_template, request, g
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

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


# define a locale selector
@babel.localeselector
def get_locale():
    """Selects the most appropriate locale to use per request.

    Executed in a request context.
    """
    # check if locale argument in query string
    args = request.args
    locale = args.get('locale', None)
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """Returns a user dictionary, or None.
    """
    args = request.args
    id = args.get('login_as', None)
    if id:
        # login_as query parameter supplied
        if id.isnumeric():
            return user.get('id', None)
    return None


@app.before_request
def before_request():
    """Do something before each request endpoint is executed.

    In request context already.
    """
    user = get_user()
    g.user = user


@app.route("/", strict_slashes=False)
def index():
    """Index page.
    """
    return render_template('3-index.html')
