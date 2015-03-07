flask-emails
============

The **flask-emails** extension is a simple way to send email messages from Flask application.
It is a wrapper for `python-emails <http://github.com/lavr/python-emails>`_.

Features
--------

- Email message abstraction with html and text part, with inline attachments, etc.
- Email body template rendering
- Email HTML body transform methods: css inlining, image inlining, etc.
- SMTP backends
- DKIM signature
- Configured via Flask application config

.. note::

        There are another flask extension `Flask-Mail <http://packages.python.org/Flask-Mail/>`_
        which solves almost same problems. I guess **flask-emails** solves little more problems.

Quickstart
----------

Add email-specific options to your flask application, for example:

.. code-block:: python

        from flask import Flask
        app = Flask(__name__)
        app.config = {'EMAIL_HOST': 'localhost', 'EMAIL_PORT': 25, 'EMAIL_TIMEOUT': 10}

Create and send email:

.. code-block:: python

        from flask.ext.emails import Message

        message = Message(html='<html><p>Hi! ...',
                          subject="Party today",
                          mail_from=("John Brown", "john@gmail.com"))
        message.attach(data=open('Event.ics', 'rb'), filename='Event.ics')

        r = message.send(mail_to=("Nick Jackson", "nick@gmail.com"))

        if r.status_code not in [250, ]:
            # message is not sent, deal with this
            ...

See more examples on `python-emails docs <https://github.com/lavr/python-emails/blob/master/README.rst#examples>`_

Configuration
-------------

By default **flask-emails** reads configuration from current Flask application config
when you first time create :meth:`~Message` object.

It reads the following variables:

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

=============================== ==================================================================
``EMAIL_HOST``                  The host to use for sending email.

                                Default: ``'localhost'``

``EMAIL_PORT``                  Port to use for the SMTP server defined in ``EMAIL_HOST``.

                                Default: ``25``

``EMAIL_HOST_USER``             Username to use for the SMTP server defined in ``EMAIL_HOST``.
                                If empty, emails won’t attempt authentication.

                                Default: empty

``EMAIL_HOST_PASSWORD``         Password to use for the SMTP server defined in ``EMAIL_HOST``.
                                This setting is used in conjunction with ``EMAIL_HOST_USER`` when authenticating to the SMTP server.

                                Default: empty

``EMAIL_USE_TLS``               Whether to use a TLS (secure) connection when talking to the SMTP server.
                                This is used for explicit TLS connections, generally on port 587.
                                If you are experiencing hanging connections, see the implicit TLS setting ``EMAIL_USE_SSL``.

                                Default: ``False``

``EMAIL_USE_SSL``               Whether to use an implicit TLS (secure) connection when talking to the SMTP server.
                                In most email documentation this type of TLS connection is referred to as SSL.
                                It is generally used on port 465.
                                If you are experiencing problems, see the explicit TLS setting ``EMAIL_USE_TLS``.

                                Note that ``EMAIL_USE_TLS``/``EMAIL_USE_SSL`` are mutually exclusive, so only set one
                                of those settings to ``True``.

                                Default: ``False``

``EMAIL_SSL_CERTFILE``          If ``EMAIL_USE_SSL`` is True, you can optionally specify the path
                                to a PEM-formatted certificate chain file to use for the SSL connection.

                                Default: ``None``

``EMAIL_SSL_KEYFILE``           If ``EMAIL_USE_SSL`` is ``True``, you can optionally specify the path
                                to a PEM-formatted private key file to use for the SSL connection.

                                Note that setting ``EMAIL_SSL_CERTFILE`` and ``EMAIL_SSL_KEYFILE`` doesn’t result
                                in any certificate checking. They’re passed to the underlying SSL connection.

                                Please refer to the documentation of Python’s ``ssl.wrap_socket()`` function
                                for details on how the certificate chain file and private key file are handled.

                                Default: ``None``

``EMAIL_TIMEOUT``               Specifies a timeout in seconds for blocking operations like the connection attempt.

                                Default: ``30``

``EMAIL_SMTP_DEBUG``            Be verbose on smtp commands. The same as ``debug`` parameter in ``smtplib.SMTP``

                                Default: ``0``

``EMAIL_BACKEND``               The backend class to use for sending emails.
                                Available backends are default ``emails.backend.stmp.SMTPBackend`` and ``flask_emails.backend.DummyBackend`` (which do not send anything, useful for testing environments).

                                Default: ``emails.backend.SMTPBackend``



=============================== ==================================================================


Install
-------

Install flask-emails from pypi:

::

        $ pip install flask-emails

Links
-----

 * documentation: `flask-emails.readthedocs.org <http://flask-emails.readthedocs.org/>`_
 * python-emails: `github.com/lavr/python-emails <http://github.com/lavr/python-emails>`_
