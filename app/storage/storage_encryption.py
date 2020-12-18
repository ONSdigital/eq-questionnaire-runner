import hashlib

import simplejson as json
from jwcrypto import jwe, jwk
from jwcrypto.common import base64url_encode
from structlog import get_logger

from app.utilities.strings import to_bytes, to_str

logger = get_logger()


class StorageEncryption:
    def __init__(self, user_id, user_ik, pepper):
        if not user_id:
            raise ValueError("user_id not provided")
        if not user_ik:
            raise ValueError("user_ik not provided")
        if not pepper:
            raise ValueError("pepper not provided")

        self.key = self._generate_key(user_id, user_ik, pepper)

    @staticmethod
    def _generate_key(user_id, user_ik, pepper):
        sha256 = hashlib.sha256()
        sha256.update(to_str(user_id).encode("utf-8"))
        sha256.update(to_str(user_ik).encode("utf-8"))
        sha256.update(to_str(pepper).encode("utf-8"))

        # we only need the first 32 characters for the CEK
        cek = to_bytes(sha256.hexdigest()[:32])

        password = {"kty": "oct", "k": base64url_encode(cek)}

        return jwk.JWK(**password)

    def encrypt_data(self, data):
        if isinstance(data, dict):
            data = json.dumps(data, for_json=True)

        protected_header = {"alg": "dir", "enc": "A256GCM", "kid": "1,1"}

        jwe_token = jwe.JWE(
            plaintext=data, protected=protected_header, recipient=self.key
        )

        return jwe_token.serialize(compact=True)

    def decrypt_data(self, encrypted_token):
        jwe_token = jwe.JWE(algs=["dir", "A256GCM"])
        jwe_token.deserialize(encrypted_token, self.key)

        return jwe_token.payload
