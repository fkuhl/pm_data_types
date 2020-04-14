from pm_data_types.member import Member, MemberStatus, Transaction, TransactionType
from pm_data_types.address import Address
from pm_data_types.household import Household
from datetime import date
import jsonpickle

mem1 = Member()
mem1.family_name = "Hornswoggle"
mem1.date_of_birth = date(1776, 4, 4)
mem1.status = MemberStatus.COMMUNING
trans1 = Transaction()
trans1.date = date(1999, 1, 1)
trans1.type = TransactionType.BIRTH
mem1.transactions = [trans1]
print(f"mem1 is {mem1.member_id}")
mem1.member_id = ""
print(f"mem1 is {mem1.member_id}")

house = Household()
house.id = "xyz"
house.head = mem1

pickled = jsonpickle.encode(house)
print(pickled)
recons = jsonpickle.decode(pickled)
print(recons.head.family_name)
