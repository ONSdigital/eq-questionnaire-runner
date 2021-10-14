from app.submitter.previously_submitted_exception import PreviouslySubmittedException


def test_previously_submitted_exception():
    previously_submitted_exception = PreviouslySubmittedException("test")
    assert str(previously_submitted_exception) == "test"
