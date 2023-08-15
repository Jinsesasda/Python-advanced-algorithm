from __future__ import annotations
import copy
import json
import math
from typing import List


# Node Class
# You may make minor modifications.

class Node():
    def  __init__(self,
                  key        = None,
                  value      = None,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,
                  size = None
                 ):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent
        self.size = 1

       

 
        

# Scapegoat Tree Class.
# DO NOT MODIFY.
class SGtree():
    def  __init__(self,
                  a    : int  = None,
                  b    : int  = None,
                  m    : int  = None,
                  n    : int  = None,
                  root : Node = None):
        self.m     = 0
        self.n     = 0
        self.a     = a
        self.b     = b
        self.root  = None

    def treeheight(self) -> int:
        if self.root is None:
            return -1
        else:
            return self._treeheight(self.root)

    def treeheight(self) -> int:
        if self.root is None:
            return 0
        else:
            return self._max_depth(self.root, 0)

    def _max_depth(self, node: Node, depth: int) -> int:
        if node is None:
            return depth
        else:
            left_depth = self._max_depth(node.leftchild, depth+1)
            right_depth = self._max_depth(node.rightchild, depth+1)
            return max(left_depth, right_depth)
      

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "k": node.key,
                "v": node.value,
                "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)
             
    
    
    

    def insert(self, key: int, value: str):
        
        # Helper function to find the depth of a node
        node = Node(key=key, value=value)
        if self.root is None:
            self.root = node
            self.n += 1
            self.m = math.floor(math.log(self.n,self.a/self.b)*-1)
            
            
            return
            
        else:
            self._insert(node, self.root)
            
            self.n += 1
            self._check()
            
          
        
      
    def _insert(self, node: Node, parent: Node):
        if node.key < parent.key:
            if parent.leftchild is None:
                parent.leftchild = node
                node.parent = parent
            else:
                self._insert(node, parent.leftchild)
        else:
            if parent.rightchild is None:
                parent.rightchild = node
                node.parent = parent
            else:
                self._insert(node, parent.rightchild)

            # If the number of nodes in the tree has exceeded the upper limit of the tree size based on the α value, rebalance the tree starting from the root.
    def _check(self):

            if self.treeheight()-1  > math.log(self.n, self.b/self.a):
                self.m = math.floor(math.log(self.n,self.a/self.b)*-1)
                noded = self.deepest_node()
              
                
                self.update_size(noded)
                
               
                self.rebalance(noded)
     
            
            # Increase n by 1.
            else:
                return
            
          
    def deepest_node(self) -> Node:
        """
        Returns the deepest node in the tree.
        """
        deepest = None
        deepest_depth = -1
        stack = [(self.root, 0)]
        while stack:
            node, depth = stack.pop()
            if node is None:
                continue
            if depth > deepest_depth:
                deepest = node
                deepest_depth = depth
            stack.append((node.leftchild, depth + 1))
            stack.append((node.rightchild, depth + 1))
        return deepest           

        
    def rebalance(self, node: Node) -> Node:
    # Step 1: Find the root of the tree to be rebalanced.
       
        temp = Node() 
        temp = node
        
        while node.parent is not None and self.update_size(node) / self.update_size(node.parent) < self.a/ self.b:
          
            node = node.parent
            temp = temp.parent
            
       
        # Step 3: Rebuild the tree from the sorted list.
        tempnode = temp.parent
   
        temph = copy.deepcopy(tempnode)
        
     
    
        
     
  
        temph = copy.deepcopy(tempnode)   
             
        p = self.get_all_nodes(node.parent)
        p.sort(key=lambda node: node.key)
        new_tree = copy.deepcopy(p)
  
        
        new_root = self.build_balanced_tree(new_tree)
        if tempnode.key == self.root.key:
            self.root = new_root
        else: 
            
            if temph.parent.key > new_root.key:
                temph = temph.parent
                  
                tempnode.parent.leftchild = new_root
            else:
                
                tempnode.parent.rightchild = new_root
         

    

        return
    
    def put_new_root(self, old_root: Node, new_root: Node) -> None:
        if old_root.parent is None:
            self.root = new_root
        elif old_root == old_root.parent.leftchild:
            old_root.parent.leftchild = new_root
        else:
            old_root.parent.rightchild = new_root
        new_root.parent = old_root.parent

    def build_balanced_tree(self, nodes: List[Node]) -> Node:
        if not nodes:
            return None
        
        # Find the middle index of the list of nodes.
        mid = 0
        # Find the middle index of the list of nodes.
        if len(nodes) % 2 == 0:
          mid = len(nodes) // 2+1
        else:
            mid = len(nodes) //2
        
        # Create a new node for the middle element and make it the root of the subtree.
        root = nodes[mid]
        
        # Recursively build the left and right subtrees from the elements to the left and right of the middle element.
        root.leftchild = self.build_balanced_tree(nodes[:mid])
        root.rightchild = self.build_balanced_tree(nodes[mid+1:])
        
        # Set the parent node of the left and right subtrees.
        if root.leftchild is not None:
            root.leftchild.parent = root
        if root.rightchild is not None:
            root.rightchild.parent = root
        
        # Return the root of the subtree.
        return root

    def get_all_nodes(self,root: Node) -> List[Node]:
        nodes_list = []
        if root is None:
            return nodes_list
        stack = [root]
        while stack:
            node = stack.pop()
            nodes_list.append(node)
            if node.rightchild:
                stack.append(node.rightchild)
            if node.leftchild:
                stack.append(node.leftchild)
        return nodes_list   
    
    def update_size(self, node: Node) -> int:
        if node is None:
            return 0
        node.size = 1 + self.update_size(node.leftchild) + self.update_size(node.rightchild)
        return node.size
    















    def delete(self, key: int):
        self.root = self._delete(key, self.root)
        self._check()
        
    def _delete(self, key: int, node):
        if not node:
            return None
        elif key < node.key:
            node.leftchild = self._delete(key, node.leftchild)
        elif key > node.key:
            node.rightchild = self._delete(key, node.rightchild)
        else:
            if not node.leftchild:
                return node.rightchild
            elif not node.rightchild:
                return node.leftchild
            else:
                temp = node.rightchild
                while temp.leftchild:
                    temp = temp.leftchild
                node.key = temp.key
                node.rightchild = self._delete(temp.key, node.rightchild)
        return node
 
                


    def search(self, search_key: int) -> str:
        # Fill in and tweak the return.
        """
        Searches the tree for a node with the given key, and returns its value.
        If the node is not found, returns None.
        """
        last =[]
        node = self.root
        while node is not None:
            
            if search_key == node.key:
                last.append(node.value)
                return json.dumps(last)
            elif search_key < node.key:
                last.append(node.value)
                node = node.leftchild
            else:
                last.append(node.value)
                node = node.rightchild
        
        return json.dumps(last)














# Dump the tree to a JSON object and print it.
