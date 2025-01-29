from typing import Mapping

SecretsType = Mapping[str, Mapping[str, str]]

REQUIRED_SECRETS = [
    "EQ_SERVER_SIDE_STORAGE_USER_ID_SALT",
    "EQ_SERVER_SIDE_STORAGE_USER_IK_SALT",
    "EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER",
    "EQ_SECRET_KEY",
    "EQ_RABBITMQ_USERNAME",
    "EQ_RABBITMQ_PASSWORD",
]


def validate_required_secrets(
    secrets: SecretsType, additional_required_secrets: list[str] | None = None
) -> None:
    all_required_secrets = (
        REQUIRED_SECRETS + additional_required_secrets
        if additional_required_secrets
        else REQUIRED_SECRETS
    )
    for required_secret in all_required_secrets:
        if required_secret not in secrets["secrets"]:
            raise ValueError(f"Missing Secret [{required_secret}]")


class SecretStore:
    def __init__(self, secrets: SecretsType) -> None:
        self.secrets = secrets.get("secrets", {})

    def get_secret_by_name(self, secret_name: str) -> str | None:
        return self.secrets.get(secret_name)
