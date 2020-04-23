from pm_data_types.address import Address
from pm_data_types.member import Member
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

    def __repr__(self):
        s = ''
        s+= '__id = %s\n' % self.__id
        if self.__head:
            s+= '__head = %s\n' % '%s, %s' % (self.__head.family_name, self.__head.given_name)
        if self.__spouse:
            s+= 'spouse = %s\n' % '%s, %s' % (self.__spouse.family_name, self.__spouse.given_name)
        if self.__others:
            s+= 'Household Members:\n'
            for oi in self.__others:
                s+= '\tmember id: %s\n' % oi
        s+= '__address = %s\n' % self.__address
        return s

    @staticmethod
    def make_household(household_as_dict):
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

    @property
    def id(self): return self.__id

    @id.setter
    def id(self, id): self.__id = id

    @property
    def head(self): return self.__head

    @head.setter
    def head(self, head): self.__head = head

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
