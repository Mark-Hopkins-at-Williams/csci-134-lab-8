class Location:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, loc):
        """ Replace this with your code for Question One ("Locations"). """

    def __eq__(self, loc):
        if loc == None:
            return False
        return loc.x == self.x and loc.y == self.y

    def __str__(self):
        return "<" + str(self.x) + ", " + str(self.y) + ">"

    __repr__ = __str__


class Vehicle:
    def __init__(self, starting_location):
        self.location = starting_location
        self.destination = None

    def get_location(self):
        return self.location

    def get_destination(self):
        return self.destination

    def set_destination(self, dest):
        self.destination = dest

    def advance_time(self):
        """ Replace this with your code for Question Two ("Vehicles"). """

    def __str__(self):
        result = "** vehicle at " + str(self.location)
        if self.destination != None:
            result += ", driving to " + str(self.destination)
        else:
            result += ", currently parked"
        return result + " **"

    __repr__ = __str__


class Van(Vehicle):

    def __init__(self, capacity):
        """ Replace this with your code for Question Three ("Vans"). """

    def is_available(self):
        return self.destination == None

    def is_empty(self):
        return self.cargo == 0

    def dump_cargo(self):
        self.cargo = 0

    def get_cargo(self):
        return self.cargo

    def get_current_task(self):
        return self.current_task

    def deliver(self):
        """ Replace this with your code for Question Three ("Vans"). """

    def schedule(self, destination, task):
        """ Replace this with your code for Question Three ("Vans"). """

    def refill(self):
        """ Replace this with your code for Question Four ("Warehouses"). """

    def __str__(self):
        result = "** van at " + str(self.location)
        if self.destination != None:
            result += ", driving to " + str(self.destination)
            if self.current_task == "refill":
                result += " for a refill"
            elif self.current_task == "deliver":
                result += " for a delivery"
        else:
            result += ", currently parked"
        return result + " **"

    __repr__ = __str__


class Warehouse:
    """ Replace this with your code for Question Four ("Warehouses"). """


def find_closest(location, entities):
    """ Replace this with your code for Question Five ("Proximal"). """


class Dispatcher:

    def __init__(self, warehouses):
        self.fleet = []
        self.unfilled = []
        self.warehouses = warehouses

    def hire(self, van):
        self.fleet += [van]

    def take_order(self, destination):
        self.unfilled = self.unfilled + [destination]

    def available_vans(self):
        result = []
        for van in self.fleet:
            if van.is_available() and not van.is_empty():
                result += [van]
        return result

    def advance_time(self):
        """ Replace this with your code for Question Six ("Dispatcher"). """





