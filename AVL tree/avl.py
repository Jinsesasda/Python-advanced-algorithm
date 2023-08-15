import json
from typing import List
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key        = None,
                  value      = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild
# DO NOT MODIFY
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "k": node.key,
            "v": node.value,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else 
None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else 
None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr)

def height(root: Node) -> int:
    if root is None:
        return -1
    else:
        left = height(root.leftchild)
        right = height(root.rightchild)
        return max(left, right) + 1 


def insert(root: Node, key: int, value: str) -> Node:
    if root is None:
        return Node(key, value)
    elif key < root.key:
        root.leftchild = insert(root.leftchild, key, value)
    else:
        root.rightchild = insert(root.rightchild, key, value)

    balance = height(root.leftchild) - height(root.rightchild)

    if balance < -1 and key > root.rightchild.key:
        return rotation_L(root)
    if balance > 1 and key > root.leftchild.key:
        root.leftchild = rotation_L(root.leftchild)
        return rotation_R(root)   
    if balance > 1 and key < root.leftchild.key:
        return rotation_R(root)

    if balance < -1 and key < root.rightchild.key:
        root.rightchild = rotation_R(root.rightchild)
        return rotation_L(root)

    return root

def minValue(root: Node):
        if root is None or root.leftchild is None:
            return root
        return minValue(root.leftchild)

def rotation_L(root: Node) -> Node:
    right_child = root.rightchild
    root.rightchild = right_child.leftchild
    right_child.leftchild = root
    return right_child
    
    return new_root
def rotation_R(root: Node) -> Node:
    left_child = root.leftchild
    root.leftchild = left_child.rightchild
    left_child.rightchild = root
    return left_child
# Bulk Delete.
def delete(root: Node, keys: List[int]) -> Node:
    for key in keys:
        root = helper_function_for_delete(root, key)
    return root

def helper_function_for_delete(root: Node, key: int) -> Node:
    if root is None:
        return root

    if key < root.key:
        root.leftchild = helper_function_for_delete(root.leftchild, key)
    elif key > root.key:
        root.rightchild = helper_function_for_delete(root.rightchild, key)
    else:
        # Node to be deleted has only one child or no child
        if root.leftchild is None:
            temp = root.rightchild
            root = None
            return temp

        elif root.rightchild is None:
            temp = root.leftchild
            root = None
            return temp

        # Node to be deleted has two children
        temp = get_min_value_node(root.rightchild)

        root.key = temp.key
        root.value = temp.value

        root.rightchild = helper_function_for_delete(root.rightchild, temp.key)

    if root is None:
        return root

    balance = height(root.leftchild) - height(root.rightchild) 

    if balance > 1 and get_balance(root.leftchild) >= 0:
        return rotation_R(root)
    
    if balance > 1 and get_balance(root.leftchild) < 0:
        root.leftchild = rotation_L(root.leftchild)
        return rotation_R(root)

    if balance < -1 and get_balance(root.rightchild) <= 0:
        return rotation_L(root)
    if balance < -1 and get_balance(root.rightchild) > 0:
        root.rightchild = rotation_R(root.rightchild)
        return rotation_L(root)

    return root
def get_min_value_node(node: Node) -> Node:
    while node.leftchild is not None:
        node = node.leftchild
    return node

def get_balance(root: Node) -> int:
    left_height = height(root.leftchild)
    right_height = height(root.rightchild)
    return left_height - right_height


def get_min_value_node(root: Node) -> Node:
    current = root

    while current.leftchild is not None:
        current = current.leftchild

    return current
# Search.
def search(root: Node, search_key: int) -> str:
    def _search_helper(node: Node, key: int, num_keys: int) -> List:
        if node is None:
            return [num_keys, None]
        elif node.key == key:
            return [num_keys, node.value]
        elif key < node.key:
            return _search_helper(node.leftchild, key, num_keys+1)
        else:
            return _search_helper(node.rightchild, key, num_keys+1)
        
    if root is None:
        return json.dumps([0, None])
    else:
        result = _search_helper(root, search_key, 1)
        return json.dumps(result)
# Range Query.
def rangequery(root: Node, x0: int, x1: int) -> List[str]:
    # Fill in and tweak the return.
    
    result = []
    if root is None:
        return result
    if root.key > x0:
       result += rangequery(root.leftchild, x0, x1)
    if root.key >= x0 and root.key <= x1:
        result.append(root.value)
    if root.key < x1:
        result += rangequery(root.rightchild, x0, x1)


    return result
   


