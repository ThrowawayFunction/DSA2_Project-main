import package



#Create a hash table class -- source: https://stephenagrice.medium.com/how-to-implement-a-hash-table-in-python-1eb6c55019fd
# the hash table code from the source was adapted for this scenario
class PackageHashTable:
    def __init__(self):
        self.capacity = 40 #capacity is set to 40 since there are 40 packages. capacity is the maximum number of buckets
        self.size = 0 #size is how many items are stored in the hashtable. This can be useful for setting a value to automatically recalculate the hash table later.
        self.buckets = [None] * self.capacity

    def insert(self, key, value):
        # when something is added, size needs to be incremented
        self.size += 1    
        index = self.hash_function(key)
        # Go to the package corresponding to the hash
        node = self.buckets[index]
        # If bucket is empty, create a node, add it, and return it
        if node is None:
            self.buckets[index] = Node(key, value)
            return
        # If something already exists at the index, handle a collision by attaching it to the end of the linked list
        prev = node
        while node is not None:
            prev = node
            node = node.next
        # Add a new node at the end of the list with provided key/value
        prev.next = Node(key, value)

    def find(self, key):
        index = self.hash_function(key) #calculate hash
        node = self.buckets[index] #check the bucket at the index
        while node is not None and node.key != key: #if the node's key doesn't match, traverse the linked list to find the correct one
            node = node.next
        if node is None: #return null if none of the nodes match
            return None
        else:
            return node.value #return the value of the node with matching key
        
     #this functions pretty much the same as find, but it just deletes the node if it finds it   
    def remove(self, key):
        bucket = hash(key) % len(self.table) 
        bucket_list = self.table[bucket]
        #removes the item if it is present
        if key in bucket_list:
            bucket_list.remove(key)   
        self.size -= 1; # decrease in size
    

    def hash_function(self, key):
        return hash(key) % self.capacity #simple has function using python build in hash and the desired capacity

# nodes are used to create a linked list in the event of a hash collision. the 'value' field will be used to store packages
class Node():
    def __init__(self, key, value):
        self.key = key #the key value, necessary to be able to resolve hash collisions by verifying that we are returning the correct node in a bucket
        self.value = value # the value itself. This will be package object
        self.next = None # the next node in a bucket- only gets a value if there is a hash collision