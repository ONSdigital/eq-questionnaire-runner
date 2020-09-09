from flask import current_app
from itsdangerous import URLSafeSerializer


class URLParamSerializer(URLSafeSerializer):
    def __init__(self):
        url_param_salt = current_app.eq["secret_store"].get_secret_by_name(
            "EQ_URL_PARAM_SALT"
        )
        super().__init__(url_param_salt)
