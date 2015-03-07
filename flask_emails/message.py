# encoding: utf-8
from flask import current_app
import emails
from .config import EmailsConfig


def init_app(app):
    config = EmailsConfig(app)
    # register extension with app
    app.extensions = getattr(app, 'extensions', {})
    app.extensions['emails'] = config
    return config


class Message(emails.Message):
    """
    Send via flask app backend
    """

    @staticmethod
    def init_app(app):
        return globals()['init_app'](app)

    @classmethod
    def flask_config(cls):
        return current_app.extensions.get('emails', None) or cls.init_app(current_app)

    def __init__(self, config=None, **kwargs):
        self.config = config or self.flask_config()
        if 'mail_from' not in kwargs:
            kwargs.setdefault('mail_from', self.config.message_options.get('default_from'))
        super(Message, self).__init__(**kwargs)
        self.smtp_cls = self.config.backend_cls

    def send(self, smtp=None, **kw):
        smtp_options = {}
        smtp_options.update(self.config.smtp_options)
        if smtp:
            smtp_options.update(smtp)
        return super(Message, self).send(smtp=smtp_options, **kw)

