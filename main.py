# Student ID: 003325660
# Lucas Endres
# C950 - DSA2
# All of the CSV files are in utf-8 encoding, other encodings might not work correctly

import csv
import datetime
import packageHashTable
import packages
import truck


# define the table to put all the packages in
packageTable = packageHashTable.PackageHashTable()


################### method definitions ###################

# uses the address CSV to find the minimum distance 
def getDistance(address):
    for row in AddressCSV:
        if address in row[2]:
            return int(row[0])

#uses the distance CSV to find distances between two addresses
def distanceBetween(address1,address2):
    distance = DistanceCSV[address1][address2]
    if distance == '':
        distance = DistanceCSV[address2][address1]
    return float(distance) #convert the string value to a decimal


# method to setup each of the packages and assign the default status
def setupPackages(packageFile):

    with open(packageFile) as packagesFile:
        packagesData = csv.reader(packagesFile, delimiter = ",") #read the CSV values from the packageFile parameter, create a list
        next (packagesData)
        for p in packagesData: # loop over each package (p) in the list and assign values from the csv- status, depart time, and deliver time are not yes assigned here
            packageId = int(p[0]) #cast the string value as an int to ensure proper hashing
            packageStreet = p[1]
            packageCity = p[2]
            packageState = p[3]
            packageZip = p[4]
            packageDeadline = p[5]
            packageWeight = p[6]
            packageNotes = p[7]
            packageStatus = "At Hub"
            packagedepartTime = None
            packagedeliverTime = None

            #create a new package using the data in the list
            x = packages.Package(packageId, packageStreet, packageCity, packageState, packageZip, packageDeadline, packageWeight, packageNotes, packageStatus, packagedepartTime, packagedeliverTime)
            packageTable.insert(packageId, x)

# this is the important method that actually handles the decision making aspect of the program - input a Truck and it will use the greedy algo to find the next stop and deliver
def DeliverPackages(truck, packageTable):

    beingDelivered = [] # make a new array to keep track of which packages are being delivered - this makes it way easier to summarize results later

    # find the package in the package hash table and add it to the 'beingDelivered' array
    for assignedPackageID in truck.packageIDList:
        packageInTruck: packages.Package = packageTable.find(assignedPackageID)
        beingDelivered.append(packageInTruck)

    #while there are still packagaes in the undelivered list, keep going 
    while len(beingDelivered) > 0:
        nextAddress = 9999 # set an abitrarily high number for this value, since each distance will be compared to it
        nextPackage = None # this is the default cursor for nextPackage
        #for go through each package in the being delivered array. 
        for package in beingDelivered: #iterate over each package that needs delivered
            if package.id in [6, 25, 27, 32]: # set special instructions for package 6, 25, 27, or 32
                nextPackage = package 
                nextAddress = distanceBetween(getDistance(truck.currentLocation), getDistance(package.street)) #calculate the distance to the next package
                break
            if distanceBetween(getDistance(truck.currentLocation), getDistance(package.street)) <= nextAddress: #if the value is less than nextAddress, set that as next address and calucalte the next one again
                nextAddress = distanceBetween(getDistance(truck.currentLocation), getDistance(package.street))
                nextPackage = package
        truck.packageIDList.append(nextPackage.id)   #add nextPackage to the truck's package list 
        beingDelivered.remove(nextPackage)           #remove it from the beingDelieved list
        truck.miles += nextAddress                   #add the distance traveled to the truck's total distance traveled
        truck.currentLocation = nextPackage.street   #update the truck's location based on the travling it just did 
        truck.time += datetime.timedelta(hours=nextAddress / 18) # change the truck's time value based on the 18mph speed described in the task assignment
        nextPackage.deliverTime = truck.time # set the delivery time of the package to the time we just calculated
        nextPackage.departTime = truck.departTime # set the departure time for the package to the departure time of the truck
            
################### end method definitions ###################




################### logic for the program starts here ###################

#make a new list of values and assign it to AddressCSV  
with open("CSV/address.csv") as addressCSV:
    acsv = csv.reader(addressCSV)
    AddressCSV = list(acsv)

#make a new list of values and assign it to DistanceCSV 
with open("CSV/distance.csv") as distanceCSV:
    dcsv = csv.reader(distanceCSV)
    DistanceCSV = list(dcsv)


# call the function to actually load data from the csv files into the package table 
setupPackages('CSV/package.csv')

# create threee trucks and give them the depart times specified and some packages- packages are in ascending order
truck1 = truck.Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),[1,13,14,15,16,19,20,27,29,30,31,34,37,40])
truck2 = truck.Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),[2,3,4,5,9,18,26,28,32,35,36,38]) # all of the delayed packages or packages with notes go on truck 2- it's going to leave after truck 1 or 3 are done. Truck 2 leaves at 11 to ensure it gets all the late packages, as well as the corrected address
truck3 = truck.Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),[6,7,8,10,11,12,17,21,22,23,24,25,33,39]) 



# tell two of the trucks to leave - 1 and 3 leave because 2 has a bunch of packages with special notes. This means it can also wait for the late packages
DeliverPackages(truck1, packageTable)
DeliverPackages(truck3, packageTable)


# make sure only two trucks are out at a time. There are only two drivers
truck2.departTime = min(truck1.time, truck3.time) # truck 2 leaves when 1 or 3 are done. This ensures that late packages are covered
DeliverPackages(truck2, packageTable)


print("Western Governors University Parcel Service")

#total miles for all of the trucks
print("Truck Total Miles:", (truck1.miles + truck2.miles + truck3.miles))

while True:    
    ## allow a user to put in a time value - error handling is not implemented here so please use a real time in 24 hour format in HH:MM
    userTime = input("Please enter a time in 24 hour format like HH:MM   Input: ")

    (h, m) = userTime.split(":")
    timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
    try: ## allow a user to check the status of one pacakge by ID or all packages 
        singleEntry = [int(input("Enter a package ID (integer value from 1 to 40, inclusive) to see the status of a package. Press enter without typing anything to see all package statuses.  Input: "))]
    except ValueError:
        singleEntry =  range(1, 41)
    for packageID in singleEntry:
        package = packageTable.find(packageID)
        package.setStatus(timeChange)
        print(str(package))  