import hashlib

from flask.sessions import SecureCookieSessionInterface


class SHA256SecureCookieSessionInterface(SecureCookieSessionInterface):
    @staticmethod
    def digest_method():  # type: ignore
        return hashlib.sha256()
