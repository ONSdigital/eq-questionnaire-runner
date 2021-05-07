# 11. simplejson, orjson, python-rapidjson

## Context

Using Python 3.9.4, investigate which JSON serialization library is most appropriate.

### Candidates
- simplejson 3.17.2 (currently used)
- orjson 3.5.2
- python-rapidjson 3.5.2


## Decision

Using the test suite as a measure of success, migration to orjson and python-rapidjson was possible and were more performant than simplejson.

However the lack of support for Decimal serialization in both could lead to accuracy issues as we would have to use Float, which is a binary fraction approximation. Although a very close approximation it isn't exact. Even though tests didn't break and it seems to work with our current requirements (addition in calculated summary) it could lead to future issues if greater accuracy is required or division/rounding is introduced.

With that in mind it seems sensible to continue to use simplejson which does support Decimal serialization.


## Additional information

### Orjson changes required

- load (file-like object) replaced with

```
    with open(schema_path, "rb") as f:
        return json.loads(f.read())
```

- utf-8 encoding removed.

- for_json argument removed, but no further action was needed.

- Decimals cast to float on serialization.

- tests with list_item_id=None updated (simplejson removes them)


### python-rapidjson

- for_json argument removed, but objects must be updated to convert to JSON on serialization (Answer and Progress)

- Decimals cast to float on serialization.
