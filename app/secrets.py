EXPECTED_SECRETS = [
    "EQ_SERVER_SIDE_STORAGE_USER_ID_SALT",
    "EQ_SERVER_SIDE_STORAGE_USER_IK_SALT",
    "EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER",
    "EQ_SECRET_KEY",
    "EQ_RABBITMQ_USERNAME",
    "EQ_RABBITMQ_PASSWORD",
]


def validate_required_secrets(secrets, expected_secrets=None):
    all_expected_secrets = (
        EXPECTED_SECRETS + expected_secrets if expected_secrets else EXPECTED_SECRETS
    )
    for required_secret in all_expected_secrets:
        if required_secret not in secrets["secrets"]:
            raise Exception("Missing Secret [{}]".format(required_secret))


class SecretStore:
    def __init__(self, secrets):
        self.secrets = secrets.get("secrets", {})

    def get_secret_by_name(self, secret_name):
        return self.secrets.get(secret_name)
