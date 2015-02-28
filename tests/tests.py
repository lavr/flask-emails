# encoding: utf-8
import pytest
from nose.plugins.skip import Skip, SkipTest
from flask import Flask

SAMPLE_MESSAGE = {'html': '<p>Test from flask.ext.emails',
                  'mail_from': 's@lavr.me',
                  'mail_to': 'sergei-nko@yandex.ru',
                  'subject': 'Test from flask.ext.emails'}


def test_config():
    app = Flask(__name__)
    app.config = {'EMAIL_HOST': 'host',
                  'EMAIL_HOST_USER': 'user',
                  'EMAIL_HOST_PASSWORD': 'password',
                  'EMAIL_DEFAULT_FROM': 'a@b.com',
                  'EMAIL_UNKNOWN_OPTION': 'xxx',
                  'OTHER_OPTION': 'yyy'}

    from flask.ext.emails.config import EmailsConfig
    o = EmailsConfig(app)
    print(o.smtp_options)
    assert o.smtp_options == {u'tls': False,
                              u'debug': 0,
                              u'port': 25,
                              u'timeout': 30,
                              u'ssl': False,
                              u'host': 'host',
                              u'password': 'password',
                              u'user': 'user',
                              u'fail_silently': True}

    print(o.message_options)
    assert o.message_options == {'default_from': 'a@b.com'}

    app.config.update({'EMAIL_SSL_CERTFILE': '1.cer',
                  'EMAIL_SSL_KEYFILE': '1.key'})
    o = EmailsConfig(app)
    #print(o.smtp_options)
    assert o.smtp_options['certfile'] == '1.cer'
    assert o.smtp_options['keyfile'] == '1.key'


def test_flask_message():
    app = Flask(__name__)
    app.config.update({'EMAIL_DEFAULT_FROM': 'John Brawn <a@b.com>'})
    ctx = app.test_request_context()
    ctx.push()

    from flask.ext.emails import Message
    m = Message(html='...')
    assert m.mail_from == ('John Brawn', 'a@b.com')


def test_flask_send_dummy():
    # Send via dummy backend
    app = Flask(__name__)
    app.config.update({'EMAIL_BACKEND': 'flask_emails.backends.DummyBackend'})
    from flask.ext.emails import Message
    # Message.init_app(app)
    ctx = app.test_request_context()
    ctx.push()
    m = Message(**SAMPLE_MESSAGE)
    m.send()


def test_flask_send_real():
    # Send via real backend
    app = Flask(__name__)
    app.config.update({'EMAIL_HOST': 'mx.yandex.ru',
                       'EMAIL_FAIL_SILENTLY': False})
    from flask.ext.emails import Message
    ctx = app.test_request_context()
    ctx.push()
    # Message.init_app(app)
    m = Message(**SAMPLE_MESSAGE)
    r = m.send()
    assert r.status_code == 250
