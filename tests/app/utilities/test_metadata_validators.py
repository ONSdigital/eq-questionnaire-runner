import pytest

from app.utilities.metadata_validators import DateString


def test_deserialize_defaults_to_iso_format():
    date_string = DateString()
    assert (
        date_string._deserialize(  # pylint: disable=protected-access
            value="2014-12-22T03:12:58.019077+00:00", attr="", data=""
        )
        == "2014-12-22T03:12:58.019077+00:00"
    )


def test_deserialize_does_not_default_to_iso_format():
    date_string = DateString(format="%Y-%m-%d")
    assert (
        date_string._deserialize(  # pylint: disable=protected-access
            value="2014-12-22", attr="", data=""
        )
        == "2014-12-22"
    )


def test_deserialize_incorrect_format_errors_with_default_format():
    date_string = DateString()
    with pytest.raises(Exception) as e:
        date_string._deserialize(  # pylint: disable=protected-access
            value="2014-12-22", attr="", data=""
        )
    assert "Not a valid datetime." in str(e.value)


def test_deserialize_given_format_errors_with_wrong_format():
    date_string = DateString("%d-%m-%Y")
    with pytest.raises(Exception) as e:
        date_string._deserialize(  # pylint: disable=protected-access
            value="2023-10-22T05:16:58.019477+00:00", attr="", data=""
        )
    assert "Not a valid datetime." in str(e.value)
