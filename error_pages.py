"""Errors"""
from flask import Blueprint, render_template

from sentry import sentry_sdk

error_pages = Blueprint('error_pages', __name__)


def error(title='Unknown Error', message='Sorry, but there was an unknown error.', code=500):
    """Error template"""
    return render_template('error.html.j2', title=title, message=message), code


def bad_request(message):
    """400 error"""
    return error(title='Bad Request', message=message, code=400)


def not_authorized(message):
    """401 error"""
    return error(title='Not Authorized', message=message, code=401)


def forbidden(message):
    """403 error"""
    return error(title='Forbidden', message=message, code=403)


def page_not_found(message):
    """404 error"""
    return error(title='Page Not Found', message=message, code=404)


def internal_server_error(message):
    """500 error (with Sentry)"""
    sentry_sdk.capture_message(message, level='error')
    return error(title='Internal Server Error', message=message, code=500)


@error_pages.route('/debug-sentry', methods=['GET'])
def trigger_error():
    """Trigger error for Sentry"""
    return 1 / 0
