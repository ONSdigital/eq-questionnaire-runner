import hashlib

from flask.sessions import SecureCookieSessionInterface


class SHA256SecureCookieSessionInterface(SecureCookieSessionInterface):
    digest_method = staticmethod(hashlib.sha256)
