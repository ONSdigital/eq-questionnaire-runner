import json

from redis import Redis

from app.data_model.app_models import EQSession, UsedJtiClaim
from app.storage.datastore import TABLE_CONFIG
from app.storage.errors import ItemAlreadyExistsError


class RedisStorage:
    def __init__(self, redis: Redis):
        self.redis = redis

    def put(self, model):
        if isinstance(model, UsedJtiClaim):
            self._put_jti(model)
        elif isinstance(model, EQSession):
            self._put_session(model)
        else:
            raise NotImplementedError(
                "Only UsedJtiClaimSchema and EQSessionSchema supported"
            )

    def _put_jti(self, jti):
        record_created = self.redis.set(
            name=jti.jti_claim,
            value=int(jti.used_at.timestamp()),
            ex=int((jti.expires - jti.used_at).total_seconds()),
            nx=True,
        )

        if not record_created:
            raise ItemAlreadyExistsError()

    def _put_session(self, model):
        config = TABLE_CONFIG[type(model)]

        schema = config["schema"]()
        item = schema.dump(model)

        record_created = self.redis.set(
            name=model.eq_session_id, value=json.dumps(item), nx=False
        )

        if not record_created:
            raise ItemAlreadyExistsError()

    def get_by_key(self, model_type, key_value):
        config = TABLE_CONFIG[model_type]
        schema = config["schema"]()

        item = self.redis.get(key_value)

        if item:
            return schema.load(json.loads(item.decode("utf-8")))

    def delete(self, model):
        config = TABLE_CONFIG[type(model)]

        key_value = getattr(model, config["key_field"])

        return self.redis.delete(key_value)
