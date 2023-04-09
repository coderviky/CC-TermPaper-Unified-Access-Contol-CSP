import json
import pickle
import time
from core.models import OperationEnum

from core.poltree.poltree_classes import PolTreeNode


# function to resolve an access request
def n_ary_resolve_any(current_node: PolTreeNode, access_request, node_list):
    print("in n_ary_resolve_any()")
    # print("Entering node with attributes ",curnode.attributes)
    if current_node.decision == 'allow':
        print(f'current_node.op: {current_node.operations}')
        print(
            f"access_request['{OperationEnum.__doc__}']: {access_request[OperationEnum.__doc__]}")
        if access_request[OperationEnum.__doc__] in current_node.operations:
            return 'allow'
        else:
            return 'deny'
    i = 0
    decision = 'deny'
    print(f"current_node.value_list: {current_node.value_list}")
    for value in current_node.value_list:
        if value == access_request[current_node.attributes]:
            decision = n_ary_resolve_any(
                node_list[current_node.children[i]], access_request, node_list)
            if decision == 'allow':
                return 'allow'
        elif value == 0:
            decision = n_ary_resolve_any(
                node_list[current_node.children[i]], access_request, node_list)
            if decision == 'allow':
                return 'allow'
        i += 1
    # print("Exiting node with value 0")
    return 'deny'


def resolve_access(access_request: dict):
    infile = open("poltree.pkl", "rb")
    node_list = pickle.load(infile)
    infile.close()
    print(
        f"in resolve_access() : len(node_list): {len(node_list)} : access_request: {access_request}")

    decision = n_ary_resolve_any(node_list[0], access_request, node_list)
    print(f"decision: {decision}")
    return decision
