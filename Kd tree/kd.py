from __future__ import annotations
import heapq
import json
import math
from queue import PriorityQueue
from typing import List

# Datum class.
# DO NOT MODIFY.
class Datum():
    def __init__(self,
                 coords : List[int],
                 code   : str):
        self.coords = coords
        self.code   = code
    def to_json(self) -> str:
        dict_repr = {'code':self.code,'coords':self.coords}
        return(dict_repr)

# Internal node class.
# DO NOT MODIFY.
class NodeInternal():
    def  __init__(self,
                  splitindex : int,
                  splitvalue : int,
                  leftchild,
                  rightchild):
        self.splitindex = splitindex
        self.splitvalue = splitvalue
        self.leftchild  = leftchild
        self.rightchild = rightchild

# Leaf node class.
# DO NOT MODIFY.
class NodeLeaf():
    def  __init__(self,
                  data : List[Datum]):
        self.data = data

# KD tree class.
class KDtree():
    def  __init__(self,
                  k    : int,
                  m    : int,
                  root = None):
        self.k    = k
        self.m    = m
        self.root = root

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    # DO NOT MODIFY.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            if isinstance(node,NodeLeaf):
                return {
                    "p": str([{'coords': datum.coords,'code': datum.code} for datum in node.data])
                }
            else:
                return {
                    "splitindex": node.splitindex,
                    "splitvalue": node.splitvalue,
                    "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                    "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
                }
        if self.root is None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    # Insert the Datum with the given code and coords into the tree.
    # The Datum with the given coords is guaranteed to not be in the tree.
    def insert(self,point:tuple[int],code:str):
        # Create a new Datum object
        datum = Datum(point, code)

        if self.root is None:
            # If the tree is empty, create a new leaf node
            self.root = NodeLeaf([datum])
            return

        # Traverse the tree to find the appropriate leaf node
        node = self.root
        while isinstance(node, NodeInternal):
         
            
            
            
            if datum.coords[node.splitindex] < node.splitvalue:
                node = node.leftchild
                
            else:
                node = node.rightchild
                

        # Add the new datum to the data list of the leaf node
        node.data.append(datum)

        # If the leaf node contains more than m data objects, split it
        if len(node.data) > self.m:
            
            self._split_leaf(node)

    def _split_leaf(self, node: NodeLeaf):
 
        # Find the dimension with the maximum range among the data objects   
            ranges = [max(data.coords[i] for data in node.data) -
                  min(data.coords[i] for data in node.data) for i in range(self.k)] 
           
            splitindex = ranges.index(max(ranges))
        
            # Find the median value of the data objects along the chosen dimension
            data_sorted = sorted(node.data, key=lambda data: data.coords[splitindex])
          
            median_idx = 0
            splitvalue = 0
            left_data = None
            right_data = None
            if len(data_sorted) % 2 == 0:
                median_idx = len(data_sorted) //2-1
                splitvalue = float((data_sorted[median_idx].coords[splitindex] + data_sorted[median_idx+1].coords[splitindex]) / 2)
                left_data = data_sorted[:median_idx+1]
                right_data = data_sorted[median_idx+1:]
            else:
            
                median_idx =  (len(data_sorted) //2)
                splitvalue = float(data_sorted[median_idx].coords[splitindex])
                left_data = data_sorted[:median_idx]
                right_data = data_sorted[median_idx:]
            left_node = NodeLeaf(left_data)
            right_node = NodeLeaf(right_data)
            
            internal_node = NodeInternal(splitindex, splitvalue, left_node, right_node)
            
            # Replace the old leaf node with the new internal node in the tree
            if node == self.root:
                self.root = internal_node
            else:
               
                
                parent = self._find_parent(node)
               
        
                
                
                if parent.leftchild == node:
                    parent.leftchild = internal_node
                else:
                    parent.rightchild = internal_node
        

    def delete(self,point:tuple[int]):
    # Find the leaf node that contains the Datum with the given point coordinates
        node = self.root
        parent = None
        while isinstance(node, NodeInternal):
            parent = node
            if point[node.splitindex] < node.splitvalue:
                node = node.leftchild
            else:
                node = node.rightchild

        # Remove the Datum with the given point coordinates from the node's data list
        for i, datum in enumerate(node.data):
            if datum.coords == point:
                del node.data[i]
                break
           
     
        # 그안에 있는 노드를 다 지움. Parent 는 NodeInternal 이고 그 위에 있는 노드임. 노드는 지워야 할 데이터가 있는 리프노드임.
        if parent == self.root and len(node.data) == 0 and isinstance(parent.leftchild, NodeInternal) :
            self.root = parent.leftchild
            return
        if parent == self.root and len(node.data) == 0 and isinstance(parent.rightchild, NodeInternal) :
            self.root = parent.rightchild
            return
        
        
        if parent == self.root and len(node.data) == 0:
            if len(parent.leftchild.data) == 0:
                self.root = parent.rightchild
                parent.leftchild = None
                return
            else: 
                self.root = parent.leftchild
                parent.rightchild = None
                return
            
        # If the resulting node contains fewer than m data objects, merge it with its sibling
        if isinstance(node, NodeLeaf) and len(node.data) == 0:
            self._merge_leaf(node, parent)

    def _merge_leaf(self, node: NodeLeaf, parent: NodeInternal):
        # Find the sibling of the given node\
        if parent.leftchild == node:
            sibling = parent.rightchild
            parent.leftchild = None
        else:
            sibling = parent.leftchild
            parent.rightchild = None
            
        if parent.leftchild == None and isinstance(parent.rightchild, NodeInternal): 
            if parent.leftchild == None:
                temp = parent.rightchild
                         
            else:
                temp = parent.leftchild
             
            if temp.leftchild != None:
                    temp = temp.leftchild
            else:
                temp = temp.rightchild
            # Replace the parent node with the merged node in the tree
            if parent == self.root:
                self.root = merged_node
            else:
                grandparent = self._find_grand_parent(temp, parent)
                if grandparent.leftchild == parent:
                    grandparent.leftchild = sibling
                else:
                    grandparent.rightchild = sibling
            return             
        if parent.rightchild == node and isinstance(parent.rightchild, NodeInternal):
            sibling = parent.leftchild
            if parent.leftchild == None:
                temp = parent.rightchild               
            else:
                temp = parent.leftchild
            if temp.leftchild != None:
                    temp = temp.leftchild
            else:
                temp = temp.rightchild
            # Replace the parent node with the merged node in the tree
            if parent == self.root:
                self.root = sibling
            else:
                grandparent = self._find_grand_parent(temp, parent)
                if grandparent.leftchild == parent:
                    grandparent.leftchild = sibling
                else:
                    grandparent.rightchild = sibling            
            return 
                
        
  
        #End    
        # Merge the data lists of the node and its sibling     
        merged_data = sibling.data    
            # Merge the two leaf nodes into a new leaf node
        merged_node = NodeLeaf(merged_data)
        temp = None
        if parent.leftchild == None:
            temp = parent.rightchild
        else:
            temp = parent.leftchild

        # Replace the parent node with the merged node in the tree
        if parent == self.root:
            self.root = merged_node
        else:
            grandparent = self._find_grand_parent(temp, parent)
            if grandparent.leftchild == parent:
                grandparent.leftchild = merged_node
            else:
                grandparent.rightchild = merged_node
                
                
    def _find_parent(self, node):
        curr_node = self.root
        parent = None
        prev = self.root
        
        # Traverse the tree until we find the node or reach a leaf node
        while curr_node != node and not isinstance(curr_node, NodeLeaf):
            # Update the parent and move to the appropriate child node
            parent = curr_node
            prev = curr_node
            if node.data[0].coords[curr_node.splitindex] < curr_node.splitvalue:
                curr_node = curr_node.leftchild
            else:
                curr_node = curr_node.rightchild

        return parent    
                
    def _find_grand_parent(self, node, par):
        curr_node = self.root
        parent = None
        prev = None
        
        # Traverse the tree until we find the node or reach a leaf node
        while curr_node != par and not isinstance(curr_node, NodeLeaf):
            # Update the parent and move to the appropriate child node
            
            
            if node.data[0].coords[curr_node.splitindex] < curr_node.splitvalue:
                prev = curr_node  
                
                curr_node = curr_node.leftchild
            else:
                prev = curr_node  
                curr_node = curr_node.rightchild
             

        return prev      

    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.


    def knn(self, k: int, point: tuple[int]) -> str:
        knnlist = []
        maxheap = []
        
        # helper function to add points to knn list and max heap
        def add_point(datum):
            dist = sum((a-b)**2 for a,b in zip(point, datum.coords))
            if len(knnlist) < k:
                heapq.heappush(maxheap, (-dist, datum))
                knnlist.append(datum)
            elif dist < -maxheap[0][0]:
                _, farthest = heapq.heappushpop(maxheap, (-dist, datum))
                knnlist.remove(farthest)
                knnlist.append(datum)
        
        # helper function to recursively search for kNN
        def search(node, bounding_box):
            nonlocal leaveschecked
            if isinstance(node, NodeLeaf):
                leaveschecked += 1
                for datum in node.data:
                    add_point(datum)
            else:
                # get the splitting axis and value
                axis = node.splitindex
                value = node.splitvalue
                
                # determine which subtree is closer to the point
                if point[axis] < value:
                    near_subtree = node.leftchild
                    far_subtree = node.rightchild
                else:
                    near_subtree = node.rightchild
                    far_subtree = node.leftchild
                
                # visit the closer subtree
                search(near_subtree, bounding_box[:axis] + [(bounding_box[axis][0], value)]
                    + bounding_box[axis+1:])
                
                # check if the far subtree should be visited
                if len(knnlist) < k or (point[axis] - bounding_box[axis][0]) ** 2 \
                    < -maxheap[0][0]:
                    search(far_subtree, bounding_box[:axis] + [(value, bounding_box[axis][1])]
                        + bounding_box[axis+1:])
        
        # start recursive search from the root
        leaveschecked = 0
        search(self.root, [(float('-inf'), float('inf'))] * self.k)
        
        # sort kNN list by distance to point
        knnlist.sort(key=lambda datum: sum((a-b)**2 for a,b in zip(point, datum.coords)))
        
        # return the kNN list and leaveschecked value
        return ((json.dumps({"leaveschecked":leaveschecked+1,"points":[datum.to_json() for datum in knnlist]})))

        
 

