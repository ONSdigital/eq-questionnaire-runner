import hashlib

from jwcrypto import jwe, jwk
from jwcrypto.common import base64url_encode
from structlog import get_logger

from app.utilities.json import json_dumps
from app.utilities.strings import to_bytes, to_str

logger = get_logger()


class StorageEncryption:
    USER_ID_ERROR_MESSAGE = "user_id not provided"
    USER_IK_ERROR_MESSAGE = "user_ik not provided"
    PEPPER_ERROR_MESSAGE = "pepper not provided"

    def __init__(
        self, user_id: str | None, user_ik: str | None, pepper: str | None
    ) -> None:
        if not user_id:
            raise ValueError(self.USER_ID_ERROR_MESSAGE)
        if not user_ik:
            raise ValueError(self.USER_IK_ERROR_MESSAGE)
        if not pepper:
            raise ValueError(self.PEPPER_ERROR_MESSAGE)

        self.key = self._generate_key(user_id, user_ik, pepper)

    @staticmethod
    def _generate_key(user_id: str, user_ik: str, pepper: str) -> jwk.JWK:
        sha256 = hashlib.sha256()
        sha256.update(to_str(user_id).encode("utf-8"))
        sha256.update(to_str(user_ik).encode("utf-8"))
        sha256.update(to_str(pepper).encode("utf-8"))

        # we only need the first 32 characters for the CEK
        cek = to_bytes(sha256.hexdigest()[:32])

        password = {"kty": "oct", "k": base64url_encode(cek)}

        return jwk.JWK(**password)

    def encrypt_data(self, data: str | dict) -> str:
        if isinstance(data, dict):
            data = json_dumps(data)

        protected_header = {"alg": "dir", "enc": "A256GCM", "kid": "1,1"}

        jwe_token = jwe.JWE(
            plaintext=data, protected=protected_header, recipient=self.key
        )

        serialized_token: str = jwe_token.serialize(compact=True)
        return serialized_token

    def decrypt_data(self, encrypted_token: str) -> bytes:
        jwe_token = jwe.JWE(algs=["dir", "A256GCM"])
        jwe_token.deserialize(encrypted_token, self.key)

        payload: bytes = jwe_token.payload
        return payload
