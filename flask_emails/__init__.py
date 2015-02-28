# encoding: utf-8
from flask import current_app
import emails

__version__ = '0.3.7'

"""
Example:

    from flask import Flask
    from flask.ext.emails import Message

    app = Flask(__name__)
    Message.init_app(app)

    Message(html="...").send()

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

from .message import Message
