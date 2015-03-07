# encoding: utf-8
from __future__ import unicode_literals
from werkzeug.utils import cached_property, import_string


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
