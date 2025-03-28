
# class used to define the properties of packages
# for ease of namespace, most logic is defined directly in main.py

import datetime

class Package:
    def _init_(self, Id, street, city, state, zip, deadline, weight, notes, status, departureTime = None, deliveryTime = None):
        self.Id = Id
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departureTime = None # these aren't known until a truck leaves
        self.deliveryTime = None  # so we just set them as null for now


    # print out all the details of the package in a formatted string. similar to overriding C# ToString() method
    def _str_(self):
        return "Id: %s, %-20s, %s, %s,%s, Deadline: %s,%s,%s,Departure Time: %s,Delivery Time: %s" % (self.ID, self.street, self.city, self.state, self.zip, self.deadline, self.weight, self.status, self.departureTime, self.deliveryTime)
    

    # determines where a package is what time and prints it to the console - also handles the mid-morning address change
    def updateStatus(self, time):
        if self.time == None:
            self.status = "At Hub"
        elif time < self.deliveryTime:
            self.status = "On its way!"
        elif time <= self.departureTime:
            self.status = "At Hub"
        else:
            self.status = "Delivered!"
        if self.id == 9:  # we know that address 9 is going to change ahead of time, so special rules apply here 
            if time <= datetime.timedelta(hours = 10, minutes = 20): #check when the package is being referenced, before or after 10:20 AM, and assign the address accordingly
                self.street = "410 S State St"
                self.zip = "84111"
            else:
                self.street = "300 State St"
                self.zip = "84103"








    