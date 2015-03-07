# encoding: utf-8
from __future__ import unicode_literals
from werkzeug.utils import cached_property, import_string

"""
flask_emails reads configuration from app config.

Configuration options:

EMAIL_HOST
The host to use for sending email.
Default: 'localhost'

EMAIL_PORT
Port to use for the SMTP server defined in EMAIL_HOST.
Default: 25

EMAIL_HOST_USER
Username to use for the SMTP server defined in EMAIL_HOST. If empty, emails won’t attempt authentication.
Default: empty

EMAIL_HOST_PASSWORD
Password to use for the SMTP server defined in EMAIL_HOST. This setting is used in conjunction with EMAIL_HOST_USER when authenticating to the SMTP server.
Default: empty

EMAIL_USE_TLS
Whether to use a TLS (secure) connection when talking to the SMTP server. This is used for explicit TLS connections, generally on port 587. If you are experiencing hanging connections, see the implicit TLS setting EMAIL_USE_SSL.
Default: False

EMAIL_USE_SSL
Whether to use an implicit TLS (secure) connection when talking to the SMTP server. In most email documentation this type of TLS connection is referred to as SSL. It is generally used on port 465. If you are experiencing problems, see the explicit TLS setting EMAIL_USE_TLS.
Note that EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive, so only set one of those settings to True.
Default: False

EMAIL_SSL_CERTFILE
If EMAIL_USE_SSL is True, you can optionally specify the path to a PEM-formatted certificate chain file to use for the SSL connection.
Default: None

EMAIL_SSL_KEYFILE
If EMAIL_USE_SSL is True, you can optionally specify the path to a PEM-formatted private key file to use for the SSL connection.
Note that setting EMAIL_SSL_CERTFILE and EMAIL_SSL_KEYFILE doesn’t result in any certificate checking. They’re passed to the underlying SSL connection.
Please refer to the documentation of Python’s ssl.wrap_socket() function for details on how the certificate chain file and private key file are handled.
Default: None

EMAIL_TIMEOUT
Specifies a timeout in seconds for blocking operations like the connection attempt.
Default: 30

EMAIL_SMTP_DEBUG
Default: 0
See debug parameter in smtplib.SMTP
"""

def get_namespace(obj, namespace, valid_keys=None):
    rv = {}
    for k in obj:
        if not k.startswith(namespace):
            continue
        key = k[len(namespace):].lower()
        if valid_keys and key not in valid_keys:
            continue
        v = obj[k]
        rv[key] = v
    return rv


class EmailsConfig:
    """
    Configuration wrapper reads EMAIL_* options from Flask application config.
    """

    _default_smtp_options = {
        'host': 'localhost',
        'port': 25,
        'host_user': '',
        'host_password': '',
        'use_tls': False,
        'use_ssl': False,
        'timeout': 30,
        'ssl_certfile': None,
        'ssl_keyfile': None,
        'smtp_debug': 0,
        'fail_silently': True
    }

    _default_message_options = {
        'default_from': None
    }

    _default_backend_options = {
        'backend': 'emails.backend.smtp.SMTPBackend'
    }

    def __init__(self, app=None, config=None):
        """
        Gets configuration options from Flask **app** object and dict-like **config** parameter.

        Parameters from **config** overrides **app** config options.
        """
        self._config = {}
        self._app = app
        if app:
            self._app = app
            self._config = app.config
        if config:
            self._config.update(config)

    @cached_property
    def options(self):
        """
        Reads all EMAIL_ options and set default values.
        """
        config = self._config
        o = {}
        o.update(self._default_smtp_options)
        o.update(self._default_message_options)
        o.update(self._default_backend_options)
        o.update(get_namespace(config, 'EMAIL_', valid_keys=o.keys()))
        o['port'] = int(o['port'])
        o['timeout'] = float(o['timeout'])
        return o

    @cached_property
    def smtp_options(self):
        """
        Convert config namespace to emails.backend.SMTPBackend namespace
        Returns dict for SMTPFactory
        """
        o = {}
        options = self.options
        for key in self._default_smtp_options:
            if key in options:
                o[key] = options[key]

        o['user'] = o.pop('host_user', None)
        o['password'] = o.pop('host_password', None)
        o['tls'] = o.pop('use_tls', False)
        o['ssl'] = o.pop('use_ssl', False)
        o['debug'] = o.pop('smtp_debug', 0)
        for k in ('certfile', 'keyfile'):
            v = o.pop('ssl_'+k, None)
            if v:
                o[k] = v
        return o

    @cached_property
    def message_options(self):
        """
        Convert config namespace to emails.Message namespace
        """
        o = {}
        options = self.options
        for key in self._default_message_options:
            if key in options:
                o[key] = options[key]
        return o

    @cached_property
    def backend_cls(self):
        return import_string(self.options['backend'])
