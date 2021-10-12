import unittest

from app.submitter.previously_submitted_exception import PreviouslySubmittedException


class PreviouslySubmittedExceptionTest(unittest.TestCase):
    def test(self):
        previously_submitted_exception = PreviouslySubmittedException("test")
        self.assertEqual("test", str(previously_submitted_exception))


if __name__ == "__main__":
    unittest.main()
