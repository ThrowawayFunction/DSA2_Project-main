
# class used to define the properties of packages
# for ease of namespace, most logic is defined directly in main.py

import datetime

class Package():

    def __init__(self, ID, street, city, state, zip, deadline, weight, notes, status, departTime, deliverTime):
        self.id = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departTime = None # these aren't known until a truck leaves
        self.deliverTime = None  # so we just set them as null for now



    # print out all the details of the package in a formatted string. similar to overriding C# ToString() method
    def __str__(self):
        return "ID: %-3s, %-42s, %-30s, %-3s, %-8s, Deadline: %-5s, %-15s, %s, Departed At: %s,  Was or will be delivered at: %s" % (self.id, self.street, self.city, self.state, self.zip, self.deadline, self.weight, self.status, self.departTime, self.deliverTime)
    

    # determines where a package is what time and prints it to the console - also handles the mid-morning address change
    def setStatus(self, time):
        if self.deliverTime == None:
            self.status = "At Hub"
        elif time < self.deliverTime:
            self.status = "On its way!"
        elif time <= self.departTime:
            self.status = "At Hub"
        else:
            self.status = "Delivered!"
        if self.id == 9:  # we know that address 9 is going to change ahead of time, so special rules apply here 
            if time <= datetime.timedelta(hours = 10, minutes = 20): #check when the package is being referenced, before or after 10:20, and assign the address accordingly
                self.street = "410 S State St"
                self.zip = "84111"
            else:
                self.street = "300 State St"
                self.zip = "84103"








    