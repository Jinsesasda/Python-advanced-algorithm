import json

# DO NOT MODIFY THIS CLASS!
class Node():
    def  __init__(self, 
                  key        = None, 
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY THIS FUNCTION!
# For the tree rooted at root, dump the tree to stringified JSON object and return.
# NOTE: in future projects you'll need to write the dump code yourself,
# but here it's given to you.
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:    
        return {
            "k": node.key,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr)

#---------------------------------------------------------------------------------------------------

# For the tree rooted at root, insert the given key and return the root node.
# The key is guaranteed to not be in the tree.
def insert(root: Node, key: int) -> Node:
    # YOUR CODE GOES HERE.
    if root is None:
        return Node(key)
    else:
        if root.key == key:
            return root
        elif root.key < key:
            root.rightchild = insert(root.rightchild, key)
        else:
            root.leftchild = insert(root.leftchild, key)
                    
        return root

# For the tree rooted at root, delete the given key and return the root node.
# The key is guaranteed to be in the tree.
# When replacement is necessary use the inorder successor.
def delete(root: Node, key: int) -> Node:
    # YOUR CODE GOES HERE.
     # if root doesn't exist, just return it
    if root is None:
        return root
  
    if key < root.key:
        root.leftchild = delete(root.leftchild, key)
  
    elif(key > root.key):
        root.rightchild = delete(root.rightchild, key)
  
    # If key is same as root's key, then this is the node
    # to be deleted
    else:
  
        # Node with only one child or no child
        if root.leftchild is None:
            temp = root.rightchild
            root = None
            return temp
  
        elif root.rightchild is None:
            temp = root.leftchild
            root = None
            return temp
  
        # Node with two children: 
        temp = minValueNode(root.rightchild)
        root.key = temp.key
  
        # Delete the inorder successor
        root.rightchild = delete(root.rightchild, temp.key)
  
    return root
# For the tree rooted at root, calculate the list of keys on the path from the root to the search key.
# Return the json stringified list.
# The key is guaranteed to be in the tree.
def search(root: Node, search_key: int) -> str:
    # YOUR CODE GOES HERE.
    # Then tweak the next line so it uses your list rather than None.
    key_list = []
    helpersearch(root, key_list,search_key)
    
    return(json.dumps(key_list))
def helpersearch(root:Node, key_list, search_key):
    key_list.append(root.key)
    if search_key == root.key:
     return
 
    if search_key > root.key:
        helpersearch(root.rightchild,key_list,search_key)
    else:
        helpersearch(root.leftchild, key_list, search_key)   

# For the tree rooted at root, dump the preorder traversal to a stringified JSON list and return.
def preorder(root: Node) -> str:
    # YOUR CODE GOES HERE.
    # Then tweak the next line so it uses your list rather than None.
     # YOUR CODE HERE
    key_list = []
    preorderHelper(root, key_list)
    return(json.dumps(key_list))
def preorderHelper(root:Node, list):
        if not root:
            return

        list.append(root.key)
        preorderHelper(root.leftchild, list)
        preorderHelper(root.rightchild, list)

# For the tree rooted at root, dump the inorder traversal to a stringified JSON list and return.
def inorder(root: Node) -> str:
    # YOUR CODE GOES HERE.
    # Then tweak the next line so it uses your list rather than None.
    key_list = []
    inorderHelper(root, key_list)
    return(json.dumps(key_list))
def inorderHelper(root:Node, list):
    if not root:
        return

    
    inorderHelper(root.leftchild, list)
    list.append(root.key)
    inorderHelper(root.rightchild, list)

# For the tree rooted at root, dump the postorder traversal to a stringified JSON list and return.
def postorder(root: Node) -> str:
    # YOUR CODE GOES HERE.
    # Then tweak the next line so it uses your list rather than None.
    key_list = []
    
    postorderHelper(root, key_list)
    return(json.dumps(key_list))
def postorderHelper(root:Node, list):
    if not root:
        return

    
    postorderHelper(root.leftchild, list)
    postorderHelper(root.rightchild, list)
    list.append(root.key)

def minValueNode(node) -> Node:
    current = node
  
    # loop down to find the leftmost leaf
    while(current.leftchild is not None):
        current = current.leftchild
  
    return current
    
# For the tree rooted at root, dump the BFT traversal to a stringified JSON list and return.
# The DFT should traverse left-to-right.
def bft(root: Node) -> str:
    
    
    queue = [root]
    values = []

    while len(queue)!=0:
    
     currentNode = queue.pop(0)
     values.append(currentNode.key)
  
    
     if currentNode.leftchild!=None:
    
      queue.append(currentNode.leftchild)
     if currentNode.rightchild!=None:
     
      queue.append(currentNode.rightchild)
    




    return json.dumps(values)  