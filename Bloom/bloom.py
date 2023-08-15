from __future__ import annotations
import json
import math
from typing import List

def hash(username:str,j:int,m:int) -> int:
    ascii_vals = [ord(char) for char in username]  # convert each character to its ASCII value
    hash_val = sum(ascii_vals)  # add the ASCII values together
    while hash_val < m:
        hash_val = int(str(hash_val) + str(hash_val))  # concatenate hash_val with itself until it's at least m
    hash_val = hash_val ** j  # raise hash_val to the j power
    hash_val_str = str(hash_val).zfill(len(str(m)))[:len(str(m))]  # make sure hash_val has the same number of digits as m
    return int(hash_val_str) % m  # take the result mod m

# Bloom Filter Class
# DO NOT MODIFY

class Bloom():
    def __init__(self,
                 m         = int,
                 k         = int,
                 fpmax     = float,
                 threshold = int,
                 bitarray  = List[int],
                 usernamedict   = dict,
                 n         = int):
        self.m         = m
        self.k         = k
        self.fpmax     = fpmax
        self.threshold = threshold
        self.bitarray  = [0] * m
        self.usernamedict   = {}
        self.n         = 0

    def dump(self) -> str:
        def _to_dict(b) -> str:
            dict_repr = ''.join([str(i) for i in self.bitarray])
            return(dict_repr)
        return(_to_dict(self.bitarray))

    # If a username has been hacked, record it.
    # If it's hacked threshold times, insert it into the bloom filter.

    
    def hack(self, username: str):
   
        if username in self.usernamedict:
            self.usernamedict[username] += 1
            
        else:
            self.usernamedict[username] = 1

           
        if self.usernamedict[username] == self.threshold:
            self.insert(username)
        elif self.usernamedict[username] > self.threshold:
            hash_indices = [hash(username, i, self.m) for i in range(1,self.k+1)]
            for idx in hash_indices:
                self.bitarray[idx] = 1
        
        

    def insert(self, keyusername: str):
        
        for i in range(1,self.k+1):
      
           
            hash_value = hash(keyusername, i, self.m)
  
            
            self.bitarray[hash_value] = 1
        self.n += 1
       
        # Check false positive rate and rebuild if necessary
        if self.fp() > self.fpmax:
            self.rebuild()
            
        # Check false positive rate and rebuild if necessary
       

    def check(self, username:str) -> str:
        hash_indices = [hash(username, i, self.m) for i in range(1,self.k+1)]
        for idx in hash_indices:
            if self.bitarray[idx] == 0:
                return json.dumps({'username': username, 'status': 'SAFE'})
        return json.dumps({'username': username, 'status': 'UNSAFE'})

    def fp(self) -> float:
        p = (1 - (1 - 1/self.m)**(self.k*self.n))**self.k
        return p


    def rebuild(self):
        # Compute the new m value
        

        fp_desired = self.fpmax / 2  # desired false positive probability
     
        while self.fp() > self.fpmax/2:
            self.m += 1
           
        
            
     
        

        # Compute the new k value
     
     
        # Create a new Bloom filter with the new m and k values
        new_bloom = Bloom(self.m, self.k, self.fpmax, self.threshold)
        for username in self.usernamedict:
      
            if self.usernamedict.get(username) >= self.threshold:
             new_bloom.insert(username)
            
        # Insert all usernames from the old Bloom filter into the new one
 
       
        # Replace the old Bloom filter with the new one
        self.m = new_bloom.m
        self.k = new_bloom.k
        self.bitarray = new_bloom.bitarray
   




