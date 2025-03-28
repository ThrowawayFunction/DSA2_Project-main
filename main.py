# Student ID: 003325660
# Lucas Endres
# C950 - DSA2

import csv
import datetime
import packageHashTable
import package
import truck



################### method definitions ###################

# uses the address CSV to find the minimum distance 
def addresss(address):
    for row in AddressCSV:
        if address in row[2]:
           return int(row[0])

#uses the distance CSV to find distances between two addresses
def distanceBetween(address1,address2):
    distance = DistanceCSV[address1][address2]
    if distance == '':
        distance = DistanceCSV[address2][address1]
    return float(distance)


# method to setup each of the packages and assign the default status
def setupPackages(packageFile):
    with open(packageFile) as packagesFile:
        packagesData = csv.reader(packagesFile, delimiter = ",") #read the CSV values from the packageFile parameter, create a list
        next (packagesData)
        for p in packagesData: # loop over each package (p) in the list and assign values from the csv- status, departure time, and delivery time are not yes assigned here
            packageId = p[0] #cast the string value as an int
            packageStreet = p[1]
            packageCity = p[2]
            packageState = p[3]
            packageZip = p[4]
            packageDeadline = p[5]
            packageWeight = p[6]
            packageNotes = p[7]
            packageStatus = "At Hub"
            packageDepartureTime = None
            packageDeliveryTime = None

            #create a new package using the data in the list
            x = package.Package(packageId, packageStreet, packageCity, packageState, packageZip, packageDeadline, packageWeight, packageNotes, packageStatus, packageDepartureTime, packageDeliveryTime)
            packageTable.insert(packageId, x)


# this is the important method that actually handles the decision making aspect of the program - input a Truck and it will use the greedy algo to find the next stop and deliver
def DeliverPackages(truck):

    #keep a list of packages
    undelivered = [] 

    #copy packages assigned to truck into the underway table
    for packageID in truck.packages:
        package = packageTable.find(packageID)
        undelivered.append(package)

    truck.packages.clear() #remove the pakages from the truck's assignment table, they are stored elsewhere now


    #while there are still packagaes in the undelivered list, keep going 
    while len(undelivered) > 0:
        nextAddress = 0 # just a default value for the next address, gets overwritten right away
        nextPackage = None # another default value
        for package in undelivered: # for each package which is not delivered
           
            if package.ID in [25, 6]: # 
                nextPackage = package
                nextAddress = distanceBetween(addresss(truck.currentLocation), addresss(package.street))
                break

            if distanceBetween(addresss(truck.currentLocation), addresss(package.street)) <= nextAddress:
                nextAddress = distanceBetween(addresss(truck.currentLocation), addresss(package.street))
                nextPackage = package


        truck.packages.append(nextPackage.ID)    
        undelivered.remove(nextPackage)
        truck.miles += nextAddress
        truck.currentLocation = nextPackage.street
        truck.time += datetime.timedelta(hours=nextAddress / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.departTime

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

# define the table to put all the packages in
packageTable = packageHashTable.PackageHashTable()

# call the function to actually load data from the csv files into the package table
setupPackages('CSV/package.csv')

# create threee trucks and give them the departure times specified and some packages
truck1 = truck.Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),[1,13,14,15,16,19,20,27,29,30,31,34,37,40])
truck2 = truck.Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),[2,3,4,5,9,18,26,28,32,35,36,38]) # all of the delayed packages or packages with notes go on truck 2- it's going to leave after truck 1 or 3 are done
truck3 = truck.Truck(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),[6,7,8,10,11,12,17,21,22,23,24,25,33,39]) 



# tell two of the trucks to leave - 1 and 3 leave because 2 has a bunch of packages with special notes. This means it can also wait for the late packages
DeliverPackages(truck1)
DeliverPackages(truck3)


# make sure only two trucks are out at a time. There are only two drivers
truck2.departTime = min(truck1.time, truck3.time) # truck 2 leaves when 1 or 3 are done. This ensures that late packages are covered
DeliverPackages(truck2)


print("Western Governors University Parcel Service")

#total miles for all of the trucks
print ("Truck Total Miles:", (truck1.miles + truck2.miles + truck3.miles))

while True:    
    ## allow a user to put in a time value - error handling is not implemented here so please use a real time in 24 hour format in HH:MM
    userTime = input("Please enter a time in 24 hour format like HH:MM   Input: ")
    (h, m) = userTime.split(":")
    timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
    try: ## allow a user to check the status of one pacakge by ID or all packages 
        singleEntry = [int(input("Enter a package ID (integer value from 1 to 40, inclusive) to see the status of a package. Enter no value and return to see all package status.  Input: "))]
    except ValueError:
        singleEntry =  range(1, 41)
    for packageID in singleEntry:
        package = packageTable.search(packageID)
        package.statusUpdate(timeChange)
        print(str(package))  