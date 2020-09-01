import unittest

from app.authentication.expired_token_exception import ExpiredTokenException


class ExpiredTokenExceptionTest(unittest.TestCase):
    def test(self):
        no_token = ExpiredTokenException("test")
        self.assertEqual("test", str(no_token))


if __name__ == "__main__":
    unittest.main()
