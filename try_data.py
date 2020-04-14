from pm_data_types.member import Member, MemberStatus, Transaction, TransactionType
from pm_data_types.address import Address
from pm_data_types.household import Household
from datetime import date
import jsonpickle
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

mem1 = Member()
mem1.family_name = "Hornswoggle"
mem1.date_of_birth = date(1776, 4, 4)
mem1.status = MemberStatus.COMMUNING
trans1 = Transaction()
trans1.date = date(1999, 1, 1)
trans1.type = TransactionType.BIRTH
mem1.transactions = [trans1]
pp.pprint(f"mem1 is {mem1.member_id}")
mem1.member_id = ""
pp.pprint(f"mem1 is {mem1.member_id}")

house = Household()
house.id = "xyz"
house.head = mem1

pickled = jsonpickle.encode(house)
pp.pprint(json.loads(pickled))
recons = jsonpickle.decode(pickled)
pp.pprint(recons.head.family_name)
