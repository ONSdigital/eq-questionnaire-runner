def for_json(object):
    for_json_attribute = getattr(object, "for_json", None)
    if for_json_attribute and callable(for_json_attribute):
        return object.for_json()
    raise AttributeError(
        f"Object {type(object)} does not have a callable for_json attribute"
    )
