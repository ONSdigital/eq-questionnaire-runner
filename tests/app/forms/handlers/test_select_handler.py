from app.forms.field_handlers.select_handler import SelectHandler


def test__coerce_str_unless_none():
    assert SelectHandler.coerce_str_unless_none(1) == '1'
    assert SelectHandler.coerce_str_unless_none('bob') == 'bob'
    assert SelectHandler.coerce_str_unless_none(12323245) == '12323245'
    assert SelectHandler.coerce_str_unless_none('9887766') == '9887766'
    assert SelectHandler.coerce_str_unless_none('None') == 'None'
    assert SelectHandler.coerce_str_unless_none(None) is None
