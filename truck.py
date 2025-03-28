
import packages

# class used to define the properties of trucks
# for ease of namespace, most logic is defined directly in main.py

class Truck():
    def __init__(self, speed, miles, currentLocation, departTime, packageIDList):
        self.speed = speed
        self.miles = miles
        self.currentLocation = currentLocation
        self.time = departTime
        self.departTime = departTime
        self.packageIDList = packageIDList

    # equivalent to overriding the C# ToString() method
    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.speed, self.miles, self.currentLocation, self.time, self.departTime, self.packageIDList)