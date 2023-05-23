#!/usr/bin/env python3
"""Basic Flask app.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


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


# define timezone selector
@babel.timezoneselector
def get_timezone():
    """Determine an appropriate timezone to use.

    In a request context, after before_request.

    Returns: pytz.timezone
    """
    # query string
    timezone = request.args.get('timezone', None)
    if timezone:
        try:
            return pytz.timezone(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # user settings
    user = g.user  # should be set already
    timezone = user.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # return None to fall back to config default


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
        # locale from URL query parameters; priority one
        return locale

    user = get_user()
    if user:
        locale = user.get('locale', None)
        if locale and locale in app.config['LANGUAGES']:
            # locale from user settings; priority two
            return locale

    # locale from request header; priority three
    return request.accept_languages.best_match(app.config['LANGUAGES'])


'''
babel = Babel(
        app,
        locale_selector=get_locale,
        timezone_selector=get_timezone,
        )
'''


def get_user():
    """Returns a user dictionary, or None.
    """
    args = request.args
    id = args.get('login_as', None)
    if id:
        # login_as query parameter supplied
        if id.isnumeric():
            user = users.get(int(id), None)
            return user
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
    return render_template('7-index.html')
