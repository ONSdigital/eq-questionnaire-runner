import unittest

import fakeredis
from mock import patch

from app.setup import create_app
from tests.app.mock_data_store import MockDatastore


class AppContextTestCase(unittest.TestCase):
    """
    unittest.TestCase that creates a Flask app context on setUp
    and destroys it on tearDown
    """

    LOGIN_DISABLED = False
    setting_overrides = {}

    @property
    def test_app(self):
        return self._app

    def setUp(self):
        self._ds = patch("app.setup.datastore.Client", MockDatastore)
        self._ds.start()

        self._redis = patch("app.setup.redis.Redis", fakeredis.FakeStrictRedis)
        self._redis.start()

        setting_overrides = {"LOGIN_DISABLED": self.LOGIN_DISABLED}
        setting_overrides.update(self.setting_overrides)
        self._app = create_app(setting_overrides)

        self._app.config["SERVER_NAME"] = "test.localdomain"
        self._app_context = self._app.app_context()
        self._app_context.push()

    def tearDown(self):
        self._app_context.pop()

    def app_request_context(self, *args, **kwargs):
        return self._app.test_request_context(*args, **kwargs)
