import json
from pm_data_types.data_common import BadDataError


class Address:
    """Address of Household, or temporary address of member."""

    def __init__(self):
        self.__id = 0  # used only in import from Java
        self.__address = ""
        self.__address2 = ""
        self.__city = ""
        self.__state = ""
        self.__postal_code = ""
        self.__country = ""
        self.__email = ""
        self.__home_phone = ""

    def __str__(self):
        s = f"  address: {self.__address} / {self.__address2}"
        s += f"\n    city: {self.__city} state: {self.__state} postal: {self.__postal_code}"
        if self.__country:
            s += f"\n    country: {self.__country}"
        s += f"\n    email: '{self.__email}' phone: '{self.__home_phone}''"
        return s

    @property
    def id(self): return self.__id

    @id.setter
    def id(self, newval): self.__id = newval

    @property
    def address(self): return self.__address

    @address.setter
    def address(self, address):
        if not address:
            raise BadDataError(address)
        self.__address = address

    @property
    def address2(self): return self.__address2

    @address2.setter
    def address2(self, newval): self.__address2 = newval

    @property
    def city(self): return self.__city

    @city.setter
    def city(self, newval):
        if not newval:
            raise BadDataError(newval)
        self.__city = newval

    @property
    def state(self): return self.__state

    @state.setter
    def state(self, newval): self.__state = newval

    @property
    def postal_code(self): return self.__postal_code

    @postal_code.setter
    def postal_code(self, newval):
        if not newval:
            raise BadDataError(newval)
        self.__postal_code = newval

    @property
    def country(self): return self.__country

    @country.setter
    def country(self, newval): self.__country = newval

    @property
    def email(self): return self.__email

    @email.setter
    def email(self, newval): self.__email = newval

    @property
    def home_phone(self): return self.__home_phone

    @home_phone.setter
    def home_phone(self, newval): self.__home_phone = newval
