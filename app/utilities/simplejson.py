import simplejson as json


def load_json(file):
    return json.load(file)


def loads_json(data, **kwargs):
    return json.loads(data, use_decimal=True, **kwargs)


def dumps_json(data):
    return json.dumps(data, for_json=True)
