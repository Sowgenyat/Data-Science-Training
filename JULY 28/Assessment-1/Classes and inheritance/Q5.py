class Vehicle:
    def drive(self):
        print("These are vehicles")

class Car(Vehicle):
    def drive(self):
        print("This car is one of the vehicles")


v = Vehicle()
v.drive()

c = Car()
c.drive()
