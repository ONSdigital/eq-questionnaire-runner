from flask import current_app
from itsdangerous import URLSafeSerializer


class URLSafeSerializerHandler:
    def __init__(self):
        url_param_salt = current_app.eq["secret_store"].get_secret_by_name(
            "EQ_URL_PARAM_SALT"
        )
        self.url_serializer = URLSafeSerializer(url_param_salt)

    def loads(self, value: str):
        return self.url_serializer.loads(value)

    def dumps(self, value: str):
        return self.url_serializer.dumps(value)
