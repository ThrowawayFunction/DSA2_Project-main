import packages


## code source: https://medium.com/@aleksej.gudkov/implementing-a-hash-table-in-python-a-step-by-step-guide-a7ef0f231d3c
## the hash table shown in the article is heavily adapted to this task

class PackageHashTable:

    def __init__(self): # make the default size 40
        self.size = 40
        self.table = [[] for _ in range(self.size)] #initialize the table witha bunch of empty arrays to support chaining

    def packageHash(self, packageID): #this is the hash function, it's based on the size of the table and uses modulus to calcualte where an package should go by hashing the package ID
            return hash(packageID) % self.size
        
    def insert(self, packageID, inputPackage): #hashes the package's ID to determine which bucket to put it, also edits existing packages if needed
        bucket = self.packageHash(packageID)
        for value in self.table[bucket]:
            if value[0] == packageID:
                value[1] = inputPackage
                return
        self.table[bucket].append([packageID, inputPackage])


        
    def find(self, packageID):
        bucket = self.packageHash(packageID)
        for value in self.table[bucket]:
            if value[0] == packageID:
                return value[1]
            else:
                return None

    def delete(self, packageID):
        bucket = self.packageHash(packageID)
        for i, package in enumerate(self.table[bucket]):
            if package[0] == packageID:
                del self.table[bucket][i]
                return
        print("Package not found")