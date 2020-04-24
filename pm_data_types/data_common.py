"""Things common to the PM data types."""

db_name = "perimeleon"
collection_name = "households"


class BadDataError(Exception):
    """Raised by property setters on receipt of a disallowed value."""

    def __init__(self, bad_value):
        self.bad_value = str(bad_value)
