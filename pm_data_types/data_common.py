"""Things common to the PM data types."""

import json

db_name = "perimeleon"
collection_name = "households"


class BadDataError(Exception):
    """Raised by property setters on receipt of a disallowed value."""

    def __init__(self, bad_value):
        self.bad_value = str(bad_value)


class CleanPropEncoder(json.JSONEncoder):
    """
    json encoder that reverts jsonpickle's attr names to simple form.
    clean_json_obj = json.loads(
            json.dumps(household_obk, cls=CleanPropEncoder))
    """
    types = []

    # List all the types that might appear in json string

    def clean_prop_name(self, k):
        for type in CleanPropEncoder.types:
            k = k.replace("_%s__" % type.__name__, "")
        return k

    # pylint: disable=method-hidden
    def default(self, obj):
        res = {self.clean_prop_name(k): v for k, v in obj.__dict__ .items()}
        if hasattr(obj, 'is_active'):
            res['is_active'] = obj.is_active
        if hasattr(obj, 'full_name'):
            res['full_name'] = obj.full_name
        return res
