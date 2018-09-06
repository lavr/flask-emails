# encoding: utf-8

__version__ = '0.4.2'

"""
Example:

    from flask import Flask
    from flask_emails import Message

    app = Flask(__name__)

    Message(html="...").send()
"""

from .message import Message, init_app
from .config import EmailsConfig