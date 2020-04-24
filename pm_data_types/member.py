from enum import Enum
from datetime import date
import uuid
from pm_data_types.address import Address
from pm_data_types.data_common import BadDataError


class TransactionType(Enum):
    BIRTH = 1
    PROFESSION = 2
    RECEIVED = 3
    SUSPENDED = 4
    SUSPENSION_LIFTED = 5
    EXCOMMUNICATED = 6
    RESTORED = 7
    DISMISSAL_PENDING = 8
    DISMISSED = 9
    REMOVED_ADMIN = 10
    DIED = 11


class Transaction:
    """One 'life event' for a Member."""

    def __init__(self):
        self.__id = ""  # irrelevant artifact of Java PeriMeleon?
        self.__date = "1970-01-01"
        self.__type = TransactionType.BIRTH.name
        self.__authority = ""
        self.__church = ""
        self.__comment = ""

    def __str__(self):
        s = f"  trans: {self.__type} date: {self.__date}"
        s += f"\n    auth: '{self.__authority}' church: '{self.__church}' comment: '{self.__comment}'"
        return s

    @property
    def id(self): return self.__id

    @id.setter
    def id(self, newval): self.__id = newval

    @property
    def date(self): return date.fromisoformat(self.__date)

    @date.setter
    def date(self, newval):
        if not newval:
            raise BadDataError(newval)
        self.__date = newval.isoformat()

    @property
    def type(self): return TransactionType[self.__type]

    @type.setter
    def type(self, newval):
        if not newval:
            raise BadDataError(newval)
        self.__type = newval.name

    @property
    def authority(self): return self.__authority

    @authority.setter
    def authority(self, newval): self.__authority = newval

    @property
    def church(self): return self.__church

    @church.setter
    def church(self, newval): self.__church = newval

    @property
    def comment(self): return self.__comment

    @comment.setter
    def comment(self, newval): self.__comment = newval


class ServiceType(Enum):
    ORDAINED_TE = 1
    ORDAINED_RE = 2
    ORDAINED_DE = 3
    INSTALLED_TE = 4
    INSTALLED_RE = 5
    INSTALLED_DE = 6
    REMOVED = 7
    EMERITUS = 8
    HON_RETIRED = 9
    DEPOSED = 10


class Service:
    """Record of an ordination or term of service as an officer."""

    def __init__(self):
        self.__index = ""  # irrelevant artifact of Java PeriMeleon?
        self.__date = "1970-01-01"
        self.__type = ServiceType.ORDAINED_RE.name
        self.__place = ""
        self.__comment = ""

    def __str__(self):
        s = f"  svc: {self.__type} date: {self.__date}"
        s += f"\n    place: '{self.__place}' comment:'{self.__comment}'"
        return s

    @property
    def index(self): return self.__index

    @index.setter
    def index(self, newval): self.__index = newval

    @property
    def date(self): return date.fromisoformat(self.__date)

    @date.setter
    def date(self, newval):
        if not newval:
            raise BadDataError(newval)
        self.__date = newval.isoformat()

    @property
    def type(self): return ServiceType[self.__type]

    @type.setter
    def type(self, newval):
        if not newval:
            raise BadDataError(newval)
        self.__type = newval.name

    @property
    def place(self): return self.__place

    @place.setter
    def place(self, newval): self.__place = newval

    @property
    def comment(self): return self.__comment

    @comment.setter
    def comment(self, newval): self.__comment = newval


class MemberStatus(Enum):
    NONCOMMUNING = 1
    COMMUNING = 2
    ASSOCIATE = 3
    EXCOMMUNICATED = 4
    SUSPENDED = 5
    DISMISSAL_PENDING = 6
    DISMISSED = 7
    REMOVED = 8
    DEAD = 9
    PASTOR = 10

    def is_active(self):
        return self == MemberStatus.NONCOMMUNING \
            or self == MemberStatus.COMMUNING \
            or self == MemberStatus.ASSOCIATE \
            or self == MemberStatus.PASTOR \
            or self == MemberStatus.SUSPENDED


class Sex(Enum):
    MALE = 1
    FEMALE = 2


class MaritalStatus(Enum):
    SINGLE = 1
    MARRIED = 2
    DIVORCED = 3


class Member:
    """Member, communing or non-communing."""

    def __init__(self):
        # every Member needs an id, but not a Mongo ID
        self.__id = str(uuid.uuid4())
        self.__family_name = ""
        self.__given_name = ""
        self.__middle_name = None
        self.__previous_family_name = None
        self.__name_suffix = None
        self.__title = None
        self.__nickname = None
        self.__sex = Sex.MALE.name
        self.__date_of_birth = "1970-01-01"
        self.__place_of_birth = ""
        self.__status = MemberStatus.COMMUNING.name
        self.__resident = True
        self.__ex_directory = False
        self.__household = ""  # id, not obj. even DEAD members have a Household
        self.__temp_address = None  # Address instance
        # Transactions: in date order because that's how they were added.
        self.__transactions = []
        self.__marital_status = MaritalStatus.SINGLE.name
        self.__spouse = ""  # name, not a member id
        self.__date_of_marriage = None  # date
        self.__divorce = ""
        self.__father = None  # member id if covenant child
        self.__mother = None  # member id if covenant child
        self.__email = None  # string
        self.__work_email = None  # string
        self.__mobile_phone = None  # string
        self.__work_phone = None  # string
        # self.__education = ""
        # self.__employer = ""
        self.__baptism = ""  # date and place as text
        self.__services = []  # Services
        self.__date_last_changed = "1970-01-01"

    def __str__(self):
        s = f"member: {self.full_name}"
        s += f"\n  {self.__status} {self.__sex} DOB: {self.__date_of_birth} place of birth: {self.__place_of_birth}"
        s += f"\n  resident: {self.__resident} ex-dir: {self.__ex_directory}"
        s += f"\n  {self.__marital_status}"
        if self.__spouse:
            s += f" spouse: {self.__spouse}"
        if self.__date_of_marriage:
            s += f" date marr: {self.__date_of_marriage}"
        if self.__divorce:
            s += f" divorce: {self.__divorce}"
        s += f"\n  baptism: {self.__baptism}"
        for t in self.__transactions:
            s += f"\n{t}"
        for sv in self.__services:
            s += f"\n{sv}"
        # TODO and at this point I'm bored...
        return s

    @property
    def id(self): return self.__id

    @id.setter
    def id(self, newval): self.__id = newval

    @property
    def family_name(self): return self.__family_name

    @family_name.setter
    def family_name(self, family_name):
        if not family_name:
            raise BadDataError(family_name)
        self.__family_name = family_name

    @property
    def given_name(self): return self.__given_name

    @given_name.setter
    def given_name(self, newval):
        if not newval:
            raise BadDataError(newval)
        self.__given_name = newval

    @property
    def middle_name(self): return self.__middle_name

    @middle_name.setter
    def middle_name(self, newval): self.__middle_name = newval

    @property
    def previous_family_name(self): return self.__previous_family_name

    @previous_family_name.setter
    def previous_family_name(
        self, newval): self.__previous_family_name = newval

    @property
    def name_suffix(self): return self.__name_suffix

    @name_suffix.setter
    def name_suffix(self, newval): self.__name_suffix = newval

    @property
    def title(self): return self.__title

    @title.setter
    def title(self, newval): self.__title = newval

    @property
    def nickname(self): return self.__nickname

    @nickname.setter
    def nickname(self, newval): self.__nickname = newval

    @property
    def sex(self):
        """Sex stored, and pickled, as enumeration name, e.g., 'MALE'"""
        return Sex[self.__sex]

    @sex.setter
    def sex(self, newval):
        if not newval:
            raise BadDataError(newval)
        self.__sex = newval.name

    @property
    def date_of_birth(self):
        """DOB stored (and pickled) as ISO format, e.g., '2010-01-02'"""
        return date.fromisoformat(self.__date_of_birth)

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth):
        if not date_of_birth:
            raise BadDataError(date_of_birth)
        self.__date_of_birth = date_of_birth.isoformat()

    @property
    def place_of_birth(self): return self.__place_of_birth

    @place_of_birth.setter
    def place_of_birth(self, newval): self.__place_of_birth = newval

    @property
    def status(self):
        return MemberStatus[self.__status]

    @status.setter
    def status(self, status):
        """Enumerations stored and pickled as name, e.g., 'COMMUNING'"""
        if not status:
            raise BadDataError(status)
        self.__status = status.name

    @property
    def resident(self): return self.__resident

    @resident.setter
    def resident(self, newval): self.__resident = newval

    @property
    def ex_directory(self): return self.__ex_directory

    @ex_directory.setter
    def ex_directory(self, newval): self.__ex_directory = newval

    @property
    def household(self): return self.__household

    @household.setter
    def household(self, newval): self.__household = newval

    @property
    def temp_address(self): return self.__temp_address

    @temp_address.setter
    def temp_address(self, newval): self.__temp_address = newval

    @property
    def transactions(self):
        return self.__transactions

    @transactions.setter
    def transactions(self, transactions):
        if not transactions:
            raise BadDataError(transactions)
        self.__transactions = transactions

    @property
    def marital_status(self): return MaritalStatus[self.__marital_status]

    @marital_status.setter
    def marital_status(self, newval):
        if not newval:
            raise BadDataError(newval)
        self.__marital_status = newval.name

    @property
    def spouse(self): return self.__spouse

    @spouse.setter
    def spouse(self, newval): self.__spouse = newval

    @property
    def date_of_marriage(self): return date.fromisoformat(
        self.__date_of_marriage)

    @date_of_marriage.setter
    def date_of_marriage(
        self, newval): self.__date_of_marriage = newval.isoformat()

    @property
    def divorce(self): return self.__divorce

    @divorce.setter
    def divorce(self, newval): self.__divorce = newval

    @property
    def father(self): return self.__father

    @father.setter
    def father(self, newval): self.__father = newval

    @property
    def mother(self): return self.__mother

    @mother.setter
    def mother(self, newval): self.__mother = newval

    @property
    def email(self): return self.__email

    @email.setter
    def email(self, newval): self.__email = newval

    @property
    def work_email(self): return self.__work_email

    @work_email.setter
    def work_email(self, newval): self.__work_email = newval

    @property
    def mobile_phone(self): return self.__mobile_phone

    @mobile_phone.setter
    def mobile_phone(self, newval): self.__mobile_phone = newval

    @property
    def work_phone(self): return self.__work_phone

    @work_phone.setter
    def work_phone(self, newval): self.__work_phone = newval

    # @property
    # def education(self): return self.__education

    # @education.setter
    # def education(self, newval): self.__education = newval

    # @property
    # def employer(self): return self.__employer

    # @employer.setter
    # def employer(self, newval): self.__employer = newval

    @property
    def baptism(self): return self.__baptism

    @baptism.setter
    def baptism(self, newval): self.__baptism = newval

    @property
    def services(self): return self.__services

    @services.setter
    def services(self, newval): self.__services = newval

    @property
    def date_last_changed(self): return date.fromisoformat(
        self.__date_last_changed)

    @date_last_changed.setter
    def date_last_changed(
        self, newval): self.__date_last_changed = newval.isoformat()

    @property
    def is_active(self):
        return self.status.is_active()

    @property
    def full_name(self):

        prev_contrib = f" ({self.previous_family_name})" if self.previous_family_name else ""
        nick_contrib = f" \"{self.nickname}\"" if self.nickname else ""
        middle_contrib = f" {self.middle_name}" if self.middle_name else ""
        suffix_contrib = f", {self.name_suffix}" if self.name_suffix else ""
        title_contrib = f" {self.title}" if self.title else ""
        return f"{self.family_name}, {self.given_name}{middle_contrib}{suffix_contrib}{title_contrib}{prev_contrib}{nick_contrib}"
