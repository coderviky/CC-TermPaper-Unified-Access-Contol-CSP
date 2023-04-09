import math
import json
import pickle
from core.models import OperationEnum
from core.poltree.poltree_classes import User, Obj, Env, entity_list, PolTreeNode

# list of nodes of poltree
node_list = list()

count = 0

# function to generate n-ary policy tree


def gen_poltree(attr_value_pair_list, available_attribute_set: set, policy_rules_list, entities: entity_list):
    '''
    Generate an n-ary policy tree

    Args:
    - attr_value_pair_list: list of tuples, list of AVP (Attribute-Value-Policy) pairs
    - available_attribute_set: set of strings, set of available attributes
    - policy_rules_list: list of dictionaries, list of rules
    - entities: object, containing user, object, and environment lists

    Returns:
    - int, id of the root node of the generated policy tree
    '''
    # available_attribute_set=attrib_set1.copy()
    # print(available_attribute_set)
    # print("in gen_poltree()")

    global count

    currrent_node = PolTreeNode(count)

    count += 1
    node_list.append(currrent_node)

    if len(available_attribute_set) == 0:
        currrent_node.decision = 'allow'
        currrent_node.operations = [
            rule[OperationEnum.__doc__] for rule in policy_rules_list]
        # currrent_node.operations = policy_rules_list[0][OperationEnum.__doc__]
        # print(f"currrent_node.op: {currrent_node.operations}")
        node_list[currrent_node.id] = currrent_node
        # print("Exiting leaf node")
        return currrent_node.id

    user_count = len(entities.user_list)
    object_count = len(entities.object_list)
    env_count = len(entities.env_list)
    # print(str(user_count)+' '+str(object_count)+' '+str(env_count))
    p = []

    for i in attr_value_pair_list:
        x = 0.0
        for ue in entities.user_list:
            # (i[0],i[1]) and
            if i[0] in ue.attributes_values_pair and ue.attributes_values_pair[i[0]] == i[1]:
                x = x+1.0/user_count
        for oe in entities.object_list:
            if i[0] in oe.attributes_values_pair and oe.attributes_values_pair[i[0]] == i[1]:
                x = x+1.0/object_count
        for ee in entities.env_list:
            if i[0] in ee.attributes_values_pair and ee.attributes_values_pair[i[0]] == i[1]:
                x = x+1.0/env_count
        if x > 0:
            p.append([i[0], i[1], x])

    max_entropy = -1.0
    max_attrib = ''
    for attrib in available_attribute_set:
        entropy = 0.0
        for x in p:
            if x[0] == attrib:
                entropy -= x[2]*(math.log(x[2])/math.log(2))
        if entropy > max_entropy:
            max_entropy = entropy
            max_attrib = attrib

    # print(f"max_attrib : {max_attrib}")
    currrent_node.attributes = max_attrib
    available_attribute_set.remove(max_attrib)
    # print(f"available_attribute_set : {available_attribute_set}")

    # finding set of values corresponding to max_attrib
    value_set = set()
    avp_list2 = list()
    # value_set.add(0)
    for i in attr_value_pair_list:
        if i[0] == max_attrib:
            value_set.add(i[1])
        else:
            avp_list2.append(i)

    # print(f"value_set : {value_set}")

    # generating policy sets of children nodes
    pol_sets = []
    for value in value_set:
        arr = list()

        for pol in policy_rules_list:
            if pol[max_attrib] == value:
                arr.append(pol)
        # print(len(arr))
        if len(arr):
            pol_sets.append(arr)
            currrent_node.value_list.append(value)

    # generating entity sets of children nodes
    entity_sets = []
    for arr in pol_sets:
        arr2 = entity_list([], [], [])
        for ue in entities.user_list:
            f = 0
            for policy in arr:
                f1 = 1
                for i in policy:
                    if i in ue.attributes_values_pair and policy[i] != ue.attributes_values_pair[i]:
                        f1 = 0
                        break
                if f1 == 1:
                    f = 1
                    break
            if f == 1:
                arr2.user_list.append(ue)

        for oe in entities.object_list:
            f = 0
            for policy in arr:
                f1 = 1
                for i in policy:
                    if i in oe.attributes_values_pair and policy[i] != oe.attributes_values_pair[i]:
                        f1 = 0
                        break
                if f1 == 1:
                    f = 1
                    break
            if f == 1:
                arr2.object_list.append(oe)

        for ee in entities.env_list:
            f = 0
            for policy in arr:
                f1 = 1
                for i in policy:
                    if i in ee.attributes_values_pair and policy[i] != ee.attributes_values_pair[i]:
                        f1 = 0
                        break
                if f1 == 1:
                    f = 1
                    break
            if f == 1:
                arr2.env_list.append(ee)
        entity_sets.append(arr2)

    i = 0
    for value in currrent_node.value_list:
        x = 0
        # print(f"len(pol_sets[{i}]) : {len(pol_sets[i])}")
        if len(pol_sets[i]) > 0:
            # print('value=', value)
            # print('No. of policies=', len(pol_sets[i]))
            x = gen_poltree(avp_list2, available_attribute_set.copy(),
                            pol_sets[i], entity_sets[i])
            currrent_node.children.append(x)
        i += 1

    node_list[currrent_node.id] = currrent_node
    # print(f'Exiting node with max attribute {max_attrib}')

    return currrent_node.id
    # return node_list


def genrate_poltree_and_save(attr_value_pair_list, available_attribute_set: set, policy_rules_list, entities: entity_list):
    global node_list
    global count
    node_list = []
    count = 0

    current_node_id = gen_poltree(attr_value_pair_list,
                                  available_attribute_set, policy_rules_list, entities)
    # print(f"node_list: {node_list[0].children}")
    # print(f"len(node_list): {len(node_list)}")
    outfile = open("poltree.pkl", "wb")
    pickle.dump(node_list, outfile, -1)
    outfile.close()

    return current_node_id
