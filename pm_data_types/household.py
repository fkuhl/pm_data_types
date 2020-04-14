from pm_data_types.address import Address
from pm_data_types.member import Member


class Household:
    """A complete household. This is the document stored in MongoDB."""

    def __init__(self):
        self.__id = ""  # the Mongo ID, we'll see what form it actually takes
        self.__head = Member()
        self.__spouse = None  # Member
        self.__others = []  # Members
        self.__address = None  # Address

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
