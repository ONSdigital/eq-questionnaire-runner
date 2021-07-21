import simplejson as json


def json_load(file, **kwargs):
    return json.load(file, use_decimal=True, **kwargs)


def json_loads(data, **kwargs):
    return json.loads(data, use_decimal=True, **kwargs)


def json_dumps(data, **kwargs):
    return json.dumps(data, for_json=True, use_decimal=True, **kwargs)
