# encoding: utf-8
from __future__ import unicode_literals, print_function
from flask import current_app

import emails
from .config import EmailsConfig


def init_app(app):
    """
    'Initialize' flask application.
    It creates EmailsConfig object and saves it in app.extensions.

    You don't have to call this method directly.

    :param app: Flask application object
    :return: Just created :meth:`~EmailsConfig` object
    """
    config = EmailsConfig(app)
    # register extension with app
    app.extensions = getattr(app, 'extensions', {})
    app.extensions['emails'] = config
    return config


class Message(emails.Message):
    """
    Email message abstraction.
    """

    def __init__(self, config=None, **kwargs):
        """
        Creates a message object. See `emails.Message` for further information.

        :param config: EmailsConfig object to use on create and send this message.
                       If `None`, use config from current flask application.

        :param kwargs: Parameters for emails.Message

        """
        self.config = config or self.flask_config
        if 'mail_from' not in kwargs:
            kwargs.setdefault('mail_from', self.config.message_options.get('default_from'))
        super(Message, self).__init__(**kwargs)
        self.smtp_cls = self.config.backend_cls

    def send(self, smtp=None, **kw):
        """
        Sends message.

        :param smtp: When set, parameters from this dictionary overwrite
                     options from config. See `emails.Message.send` for more information.

        :param kwargs: Parameters for `emails.Message.send`

        :return: Response objects from emails backend.
                 For default `emails.backend.smtp.STMPBackend` returns an `emails.backend.smtp.SMTPResponse` object.
        """
        smtp_options = {}
        smtp_options.update(self.config.smtp_options)
        if smtp:
            smtp_options.update(smtp)
        return super(Message, self).send(smtp=smtp_options, **kw)

    @staticmethod
    def init_app(app):
        return globals()['init_app'](app)

    @property
    def flask_config(self):
        return current_app.extensions.get('emails', None) or self.init_app(current_app)
