import packages


## code source: https://medium.com/@aleksej.gudkov/implementing-a-hash-table-in-python-a-step-by-step-guide-a7ef0f231d3c
## the hash table shown in the article is heavily adapted to this task

class PackageHashTable:

    def __init__(self, size=40): # make the default size 40
        self.size = size
        self.table = [[] for _ in range(size)] #initialize the table witha bunch of empty arrays to support chaining

    def packageHash(self, packageID): #this is the hash function, it's based on the size of the table and uses modulus to calcualte where an package should go by hashing the package ID
            return hash(packageID) % self.size
    
    def insert(self, packageID, inputPackage): #hashes the package's ID to determine which bucket to put it 
        bucket = self.packageHash(packageID)
        for package in self.table[bucket]:
            if package[0] == packageID:
                package[1] = inputPackage
                return
        self.table[bucket].append([packageID, inputPackage])
        
    def find(self, packageID):
        bucket = self.packageHash(packageID)
        for package in self.table[bucket]:
            if package[0] == packageID:
                return package[1]
        return None
    
    def delete(self, packageID):
        bucket = self.packageHash(packageID)
        for i, package in enumerate(self.table[bucket]):
            if package[0] == packageID:
                del self.table[bucket][i]
                return
        print("Package not found")