import simplejson as json


def load_json(file, **kwargs):
    return json.load(file, **kwargs)


def loads_json(data, **kwargs):
    return json.loads(data, use_decimal=True, **kwargs)


def dumps_json(data, **kwargs):
    return json.dumps(data, for_json=True, **kwargs)
