from core.poltree.poltree_classes import entity_list, User, Obj, Env
from employee.models import Employee
from typing import List
from core.models import PolicyRule, UserRolesEnum, ObjectTypeEnum, EnvDayEnum, Bucket, BucketObject, OperationEnum, CSPEnum, IAMDetails
from core.poltree.poltree_generator import gen_poltree, genrate_poltree_and_save
from sqlalchemy.orm import Session

from core import database
# get_db = database.get_db


####### ------- ABAC ------- #######

# # get data from db
# db: Session = get_db()


def generate_data_and_poltree_generation(db):
    print(f"in generate_data_and_poltree_generation()")

    available_attribute_set = {UserRolesEnum.__doc__,
                               ObjectTypeEnum.__doc__, EnvDayEnum.__doc__}

    # print(f"available_attribute_set: {available_attribute_set}")

    # attributes-value-pair list
    # Generate list of tuples
    attr_value_pair_list = []
    for enum_class in [UserRolesEnum, ObjectTypeEnum, EnvDayEnum]:
        for enum_member in enum_class:
            attr_value_pair_list.append(
                (enum_class.__doc__, enum_member.value))
    # result [("role","admin"),("role","auditor")....]

    # Print the generated list of tuples
    # print(f"attr_value_pair_list: {attr_value_pair_list}")

    # get user object list from db
    users: List[Employee] = db.query(Employee).all()
    # print(users)
    # convert users role to dictionary {"role": "role_name"}
    user_list = []
    for user in users:
        us = User(user.id, {UserRolesEnum.__doc__: user.role})
        user_list.append(us)
    # print(f"user_list: {user_list}")

    # get object list from db
    buckets = db.query(Bucket).all()
    bucket_list = []
    for bucket in buckets:
        buck = Obj(
            bucket.id, {ObjectTypeEnum.__doc__: ObjectTypeEnum.BUCKET.value})
        bucket_list.append(buck)

    bucket_objects = db.query(BucketObject).all()
    file_list = []
    for bucket_object in bucket_objects:
        file = Obj(
            bucket_object.id, {ObjectTypeEnum.__doc__: ObjectTypeEnum.FILE.value})
        file_list.append(file)

    object_list = bucket_list + file_list
    # print(f"object_list: {object_list}")

    # get environment list from enum
    env_list = []
    i = 0
    for day in EnvDayEnum:
        env = Env(i, {EnvDayEnum.__doc__: day.value})
        env_list.append(env)
        i += 1
    # print(f"env_list: {env_list}")

    # create entities object from enity_list class
    entities = entity_list(user_list, object_list, env_list)

    # get rules from PolicyRule table
    policy_rules: List[PolicyRule] = db.query(PolicyRule).all()
    # convert to dictionary
    policy_rules_list = []
    for rule in policy_rules:
        policy_rules_list.append({UserRolesEnum.__doc__: rule.user_role.value, ObjectTypeEnum.__doc__: rule.object_type.value,
                                  EnvDayEnum.__doc__: rule.env_day.value, OperationEnum.__doc__: rule.operation.value})

    # print(f"policy_rules_list: {policy_rules_list[0]}")

    # # call this function to generate poltree
    # current_node_id, node_list = gen_poltree(attr_value_pair_list,
    #                                          available_attribute_set, policy_rules_list, entities)
    current_node_id = genrate_poltree_and_save(attr_value_pair_list,
                                               available_attribute_set, policy_rules_list, entities)
    # print(f"current_node_id: {current_node_id}")

    # outfile = open("poltree.pkl", "wb")
    # pickle.dump(node_list, outfile, -1)
