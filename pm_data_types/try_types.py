import pymongo
import json
import pprint
from datetime import date
from pymongo import MongoClient
from pm_data_types.member import Member, MemberStatus, Sex, MaritalStatus, Transaction, TransactionType, Service, ServiceType
from pm_data_types.address import Address
from pm_data_types.household import Household
from pm_data_types.data_common import db_name, collection_name, CleanPropEncoder

db_host = "localhost"
pp = pprint.PrettyPrinter(indent=4)


def main():
    CleanPropEncoder.types = [Member, MemberStatus, Sex, MaritalStatus, Transaction,
                              TransactionType, Service, ServiceType, Address, Household]
    client = MongoClient(host=db_host, port=27017)
    db = client[db_name]
    collection = db[collection_name]
    hh_from_mongo = collection.find_one()
    # make Household instance from the dict received from Mongo
    household = Household.make_from_mongo_dict(hh_from_mongo)
    print(f"household: {household}")
    # From Household instance, make "clean" JSON for transmission to JS client.
    clean_json_obj = json.loads(household.clean_json)
    print("clean JSON obj:")
    pp.pprint(clean_json_obj)

    t_dict = clean_json_obj['head']['transactions'][1]
    print("\n\ntrans:")
    pp.pprint(t_dict)
    trans = Transaction.make_from_clean_dict(t_dict)
    print(f"type: {trans.type} date: {trans.date}")
    trans.type = TransactionType.PROFESSION
    trans.date = date.fromisoformat("1776-07-04")
    print(f"type: {trans.type} date: {trans.date}")

    m_dict = clean_json_obj['spouse']
    spouse = Member.make_from_clean_dict(m_dict)
    print(f"\n\nmem: {spouse.full_name} trans: {spouse.transactions[0]}")

    household = Household.make_from_clean_dict(clean_json_obj)
    print(f"\n\n{household}")

    member = Member.make_from_mongo_dict(hh_from_mongo["_Household__head"])
    print(f"\n\n member: {member}")
    member_clean = member.clean_json
    print(f"members clean string: {member_clean}")


if __name__ == '__main__':
    main()
