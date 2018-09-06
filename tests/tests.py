# encoding: utf-8
from nose.plugins.skip import Skip, SkipTest
import string
import random
from flask import Flask

import emails
from flask_emails.config import EmailsConfig
import flask_emails

SAMPLE_MESSAGE = {'html': '<p>Test from flask_emails',
                  'mail_from': 's@lavr.me',
                  'mail_to': 'sergei-nko@yandex.ru',
                  'subject': 'Test from flask_emails'}


def test_deault_config():
    c = EmailsConfig()
    assert c.smtp_options == {u'tls': False, u'debug': 0, u'password': u'',
                              u'ssl': False, u'host': u'localhost', u'timeout': 30,
                              u'user': u'', u'fail_silently': True, u'port': 25}
    assert c.message_options == {u'default_from': None}
    assert c.backend_cls == emails.backend.smtp.SMTPBackend


def _random_string(length=16):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                   for _ in range(length))


def test_config_smtp_options():

    default_smtp_options = EmailsConfig().smtp_options

    current_config = {}
    for config_option_name, smtp_option, value in (
            ('EMAIL_HOST', 'host', _random_string()),
            ('EMAIL_HOST_USER', 'user', _random_string()),
            ('EMAIL_HOST_PASSWORD', 'password', _random_string()),
            ('EMAIL_PORT', 'port', random.randint(0, 65000)),
            ('EMAIL_USE_SSL', 'ssl', not default_smtp_options['ssl']),
            ('EMAIL_SSL_CERTFILE', 'certfile', _random_string()),
            ('EMAIL_SSL_KEYFILE', 'keyfile', _random_string()),
            ('EMAIL_TIMEOUT', 'timeout', random.random()),
            ('EMAIL_SMTP_DEBUG', 'debug', random.randint(0, 3))
    ):
        print(config_option_name, smtp_option, value)
        current_config[config_option_name] = value
        c = EmailsConfig(config=current_config)
        print(c.smtp_options[smtp_option])
        assert c.smtp_options[smtp_option] == value


def test_config_message_options():

    current_config = {}
    for config_option_name, message_option, value in (
            ('EMAIL_DEFAULT_FROM', 'default_from', _random_string()),
    ):
        print(config_option_name, message_option, value)
        current_config[config_option_name] = value
        c = EmailsConfig(config=current_config)
        print(c.message_options[message_option])
        assert c.message_options[message_option] == value


def test_config_backend_cls():
    c = EmailsConfig(config={'EMAIL_BACKEND': 'flask_emails.backends.DummyBackend'})
    assert c.backend_cls == flask_emails.backends.DummyBackend


def test_unknown_options():
    d = EmailsConfig()
    c = EmailsConfig(config={'EMAIL_FRONTEND42': 'X', 'OTHER_OPTION': 13})
    assert c.smtp_options == d.smtp_options
    assert c.message_options == d.message_options
    assert c.backend_cls == d.backend_cls


def test_flask_message():
    app = Flask(__name__)
    app.config.update({'EMAIL_DEFAULT_FROM': 'John Brawn <a@b.com>'})
    ctx = app.test_request_context()
    ctx.push()

    from flask_emails import Message
    m = Message(html='...')
    assert m.mail_from == ('John Brawn', 'a@b.com')


def test_flask_send_dummy():
    # Send via dummy backend
    app = Flask(__name__)
    app.config.update({'EMAIL_BACKEND': 'flask_emails.backends.DummyBackend'})
    from flask_emails import Message
    # Message.init_app(app)
    ctx = app.test_request_context()
    ctx.push()
    m = Message(**SAMPLE_MESSAGE)
    m.send(smtp={'timeout': 1})


def test_flask_send_real():
    # Send via real backend
    app = Flask(__name__)
    app.config.update({'EMAIL_HOST': 'mx.yandex.ru',
                       'EMAIL_FAIL_SILENTLY': False})
    from flask_emails import Message
    ctx = app.test_request_context()
    ctx.push()
    # Message.init_app(app)
    m = Message(**SAMPLE_MESSAGE)
    r = m.send()
    assert r.status_code == 250
