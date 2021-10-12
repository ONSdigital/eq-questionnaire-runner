import unittest

from app.submitter.previously_submitted_exception import PreviouslySubmittedException


class PreviouslySubmittedExceptionExceptionTest(unittest.TestCase):
    def test(self):
        no_token = PreviouslySubmittedException("test")
        self.assertEqual("test", str(no_token))


if __name__ == "__main__":
    unittest.main()
