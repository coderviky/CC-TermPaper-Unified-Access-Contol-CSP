from typing import List

# represents a node of the policy tree


class PolTreeNode:
    '''
        Initialize a node object with given id
        Args:
        - id: int, id of the node
        '''

    def __init__(self, id):
        self.id = id
        self.attributes = None
        self.value_list = []
        self.children = []
        self.decision = 'deny'
        self.operations = []

# represents a user entity


class User:
    def __init__(self, id, attributes_values_pair: dict):
        self.id = id
        self.attributes_values_pair = dict()

# represents an object entity


class Obj:
    def __init__(self, id, attributes_values_pair: dict):
        self.id = id
        self.attributes_values_pair = dict()

# represents an environment entity


class Env:
    def __init__(self, id, attributes_values_pair: dict):
        self.id = id
        self.attributes_values_pair = dict()

# represents a list of entities, used to generate the policy tree


class entity_list:
    user_list: List[User] = []
    object_list: List[Obj] = []
    env_list: List[Env] = []

    def __init__(self, user_list: List[User], object_list: List[Obj], env_list: List[Env]):
        self.user_list = user_list
        self.object_list = object_list
        self.env_list = env_list
