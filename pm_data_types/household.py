from pm_data_types.address import Address
from pm_data_types.member import Member
from pm_data_types.data_common import BadDataError
import json
import jsonpickle


class Household:
    """A complete household. This is the document stored in MongoDB."""

    def __init__(self):
        self.__id = ""  # the Mongo ID, we'll see what form it actually takes
        self.__head = Member()
        self.__spouse = None  # Member
        self.__others = []  # Members
        self.__address = None  # Address

    def __str__(self):
        t = f"id: {self.__id} head: {self.__head.full_name}"
        if self.__spouse:
            t += f"\n  spouse: {self.__spouse.full_name}"
        t += "\n  members: "
        for other in self.__others:
            t += f" {other.given_name}"
        t += f"\n  address: {self.__address}"
        return t

    @staticmethod
    def make_from_mongo_dict(household_as_dict):
        """From a dict retrieved from Mongo, make a Household object."""
        # First do the id shuffle
        mongo_id = household_as_dict['_id']
        del household_as_dict['_id']
        household_as_dict['_Household__id'] = str(mongo_id)
        # now unpickle
        return jsonpickle.decode(json.dumps(household_as_dict))

    def mongoize(self):
        """Create a dictionary suitable for insertion into Mongo."""
        return json.loads(jsonpickle.encode(self))

    @staticmethod
    def make_from_clean_dict(dict):
        """Make Household instance from a JS-like dict."""
        household = Household()
        for k, v in dict.items():
            if k == "head":
                household.__setattr__(k, Member.make_from_clean_dict(v))
            elif k == "spouse":
                household.__setattr__(k, Member.make_from_clean_dict(v))
            elif k == "others":
                newvals = [Member.make_from_clean_dict(d) for d in v]
                household.__setattr__(k, newvals)
            elif k == "address":
                household.__setattr__(k, Address.make_from_clean_dict(v))
            else:
                household.__setattr__(k, v)
        return household

    @property
    def id(self): return self.__id

    @id.setter
    def id(self, id): self.__id = id

    @property
    def head(self): return self.__head

    @head.setter
    def head(self, head):
        if not head:
            raise BadDataError(head)
        self.__head = head

    @property
    def spouse(self): return self.__spouse

    @spouse.setter
    def spouse(self, newval): self.__spouse = newval

    @property
    def others(self): return self.__others

    @others.setter
    def others(self, newval): self.__others = newval

    @property
    def address(self): return self.__address

    @address.setter
    def address(self, newval): self.__address = newval

    @property
    def members(self):
        all_members = [self.head]
        if self.spouse:
            all_members.append(self.spouse)
        all_members.extend(self.others)
        return all_members
