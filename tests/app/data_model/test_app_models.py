import datetime

from dateutil.tz import tzutc

from app.data_models.app_models import EQSession, QuestionnaireState, UsedJtiClaim
from app.storage.storage import StorageModel
from tests.app.app_context_test_case import AppContextTestCase

NOW = datetime.datetime.now(tz=tzutc()).replace(microsecond=0)


class TestAppModels(AppContextTestCase):
    def test_questionnaire_state(self):
        new_model = self._test_model(QuestionnaireState("someuser", "somedata", 1))

        self.assertGreaterEqual(new_model.created_at, NOW)
        self.assertGreaterEqual(new_model.updated_at, NOW)

    def test_eq_session(self):
        new_model = self._test_model(
            EQSession(
                eq_session_id="sessionid",
                user_id="someuser",
                session_data="somedata",
                expires_at=NOW,
            )
        )

        self.assertGreaterEqual(new_model.created_at, NOW)
        self.assertGreaterEqual(new_model.updated_at, NOW)
        self.assertGreaterEqual(new_model.expires_at, NOW)

    def test_used_jti_claim(self):
        self._test_model(UsedJtiClaim("claimid", NOW))

    def _test_model(self, orig):
        config = StorageModel.TABLE_CONFIG[type(orig)]
        schema = config["schema"]()

        item = schema.dump(orig)
        new_model = schema.load(item)

        self.assertEqual(orig.__dict__, new_model.__dict__)

        return new_model
