import unittest

from app.authentication.no_questionnaire_state_exception import (
    NoQuestionnaireStateException,
)


class NoQuestionnaireStateExceptionTest(unittest.TestCase):
    def test(self):
        no_token = NoQuestionnaireStateException("test")
        self.assertEqual("test", str(no_token))


if __name__ == "__main__":
    unittest.main()
