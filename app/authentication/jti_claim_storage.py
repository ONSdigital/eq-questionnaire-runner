from datetime import timedelta

from flask import current_app
from structlog import get_logger

from app.data_models.app_models import UsedJtiClaim
from app.helpers.uuid_helper import is_valid_uuid
from app.storage.errors import ItemAlreadyExistsError

logger = get_logger()


class JtiTokenUsed(Exception):
    def __init__(self, jti_claim):
        super().__init__()
        self.jti_claim = jti_claim

    def __str__(self, *args, **kwargs):
        return "jti claim '{jti_claim}' has already been used".format(
            jti_claim=self.jti_claim
        )


def use_jti_claim(jti_claim, expires_at):
    """
    Use a jti claim
    :param jti_claim: jti claim to mark as used.
    :param expires_at: the datetime at which the jti claim expires.
    :raises ValueError: when jti_claim is None.
    :raises TypeError: when jti_claim is not a valid uuid4.
    :raises JtiTokenUsed: when jti_claim has already been used.
    """
    if jti_claim is None:
        raise ValueError
    if not is_valid_uuid(jti_claim):
        logger.info("jti claim is invalid", jti_claim=jti_claim)
        raise TypeError

    try:
        # Make claim expire a little later than exp to avoid race conditions with out of sync clocks.
        expires_at += timedelta(seconds=60)

        jti = UsedJtiClaim(jti_claim, expires_at)
        current_app.eq["ephemeral_storage"].put(jti, overwrite=False)
    except ItemAlreadyExistsError as e:
        logger.error("jti claim has already been used", jti_claim=jti_claim)
        raise JtiTokenUsed(jti_claim) from e
