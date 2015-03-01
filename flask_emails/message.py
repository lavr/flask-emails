# encoding: utf-8
from flask import current_app
import emails

from .config import EmailsConfig

config = None


def init_app(app):
    global config
    config = EmailsConfig(app)
    # register extension with app
    app.extensions = getattr(app, 'extensions', {})
    app.extensions['emails'] = config
    return config


class Message(emails.Message):
    """
    Send via global flask app backend
    """

    @staticmethod
    def init_app(app):
        return globals()['init_app'](app)

    def __init__(self, **kwargs):
        if 'mail_from' not in kwargs:
            kwargs.setdefault('mail_from', self.flask_config().message_options.get('default_from'))
        super(Message, self).__init__(**kwargs)
        self.smtp_cls = self.flask_config().backend_cls

    @classmethod
    def flask_config(cls):
        return current_app.extensions.get('emails', None) or cls.init_app(current_app)

    def send(self, **kw):
        global config
        smtp = kw.get('smtp')
        if smtp is None:
            kw['smtp'] = self.flask_config().smtp_options
        return super(Message, self).send(**kw)

