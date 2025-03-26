from tasks import Delivery, Refill
from addresses import Address
from manhattan import Manhattan
from vehicles import Car, Van, Helicopter

class Dispatcher:

    def __init__(self, warehouses):
        """Initializes a Dispatcher with access to specified warehouses.
        
        The `warehouses` argument is a list of Address objects (indicating
        the location of each warehouse).
        """
        self.fleet = []
        self.deliveries = []
        self.refills = []
        self.warehouses = warehouses

    def hire(self, vehicle):
        """Adds a Vehicle object to the Dispatcher's fleet."""
        self.fleet.append(vehicle)

    def take_order(self, order):
        """Accepts a new product order (i.e. a Delivery object)."""
        self.deliveries.append(order)

    def get_unfulfilled_orders(self):
        """Returns a list of product orders that haven't yet been fulfilled."""        
        return self.deliveries
    
    def assign_deliveries(self):
        """Assigns vehicles to unassigned Delivery tasks based on their ETAs."""
        for delivery in [task for task in self.deliveries if not task.already_assigned()]:
            best_vehicle = None
            best_eta = None
            for vehicle in [v for v in self.fleet if delivery.can_be_assigned_to(v)]:
                eta = vehicle.get_eta(delivery.address)
                if eta != None and (best_eta == None or eta < best_eta):
                    best_vehicle = vehicle
                    best_eta = eta            
            if best_vehicle != None:
                best_vehicle.send_to(delivery.address)
                delivery.assign_to(best_vehicle)

    def assign_refills(self):
        """Assigns a Refill task to all empty vehicles."""
        for vehicle in self.fleet:
            if vehicle.is_empty() and not vehicle.is_busy():
                best_warehouse = None
                best_eta = None
                for warehouse in self.warehouses:
                    eta = vehicle.get_eta(warehouse)
                    if eta != None and (best_eta == None or eta < best_eta):
                        best_warehouse = warehouse
                        best_eta = eta     
                if best_warehouse != None:
                    refill = Refill(best_warehouse)
                    refill.assign_to(vehicle)
                    self.refills.append(refill)
                    vehicle.send_to(best_warehouse)

    def attempt_deliveries(self):
        """Attempts to fulfill all unfulfilled delivery orders."""
        unfulfilled_deliveries = []
        for delivery in self.deliveries:
            if not delivery.attempt():
                unfulfilled_deliveries.append(delivery)
        self.deliveries = unfulfilled_deliveries

    def attempt_refills(self):
        """Attempts to fulfill all unfulfilled refill orders."""
        unfulfilled_refills = []
        for refill in self.refills:
            if not refill.attempt():
                unfulfilled_refills.append(refill)
        self.refills = unfulfilled_refills

    def dispatch(self):
        """Every time step, the Dispatcher manages its fleet of vehicles.

        Specifically, the Dispatcher:
        - assigns unassigned delivery and refill tasks,
        - updates its information on each Vehicle's location
        - attempts to fulfill any unfulfilled delivery and refill tasks
        """
        self.assign_deliveries()
        self.assign_refills()
        for vehicle in self.fleet:            
            vehicle.move()
        self.attempt_deliveries()
        self.attempt_refills()

def scenario1():
    warehouses = [Address("12", "SW"), Address("60", "NE"), Address("57", "NW")]
    dispatcher = Dispatcher(warehouses)
    return dispatcher

def scenario2():
    warehouses = [Address("12", "SW"), Address("60", "NE"), Address("57", "NW")]
    dispatcher = Dispatcher(warehouses)
    dispatcher.hire(Car(Address("14", "SE")))
    dispatcher.take_order(Delivery(Address("59", "NW")))
    return dispatcher

def scenario3():
    warehouses = [Address("12", "SW"), Address("60", "NE")]
    dispatcher = Dispatcher(warehouses)
    dispatcher.hire(Car(Address("14", "SE")))
    dispatcher.take_order(Delivery(Address("59", "NW")))
    dispatcher.take_order(Delivery(Address("36", "SW")))
    return dispatcher

def scenario4():
    warehouses = [Address("12", "SW"), Address("60", "NE")]
    dispatcher = Dispatcher(warehouses)
    dispatcher.hire(Van(Address("14", "SE"), 3))
    dispatcher.take_order(Delivery(Address("59", "NW")))
    dispatcher.take_order(Delivery(Address("58", "SW")))
    dispatcher.take_order(Delivery(Address("45", "SW")))
    dispatcher.take_order(Delivery(Address("24", "SW")))
    return dispatcher

def scenario5():
    warehouses = [Address("72", "SW"), Address("60", "NE")]
    dispatcher = Dispatcher(warehouses)
    dispatcher.hire(Helicopter(Address("13", "SE"), 1))
    dispatcher.take_order(Delivery(Address("57", "NW")))
    return dispatcher

def run_live_demo():
    dispatcher = Dispatcher([Address("12", "SW"), Address("60", "NE"), Address("57", "NW")])
    dispatcher.hire(Car(Address("14", "SE")))
    dispatcher.hire(Car(Address("22", "SW")))
    dispatcher.hire(Car(Address("57", "NW")))
    dispatcher.hire(Car(Address("10", "NE")))
    dispatcher.hire(Car(Address("60", "SE")))
    dispatcher.hire(Van(Address("50", "SW"), capacity=5))
    dispatcher.hire(Van(Address("30", "SW"), capacity=5))
    dispatcher.hire(Helicopter(Address("19", "NE"), 1))
    dispatcher.hire(Helicopter(Address("70", "SW"), 1))    
    dispatcher.hire(Helicopter(Address("50", "SE"), 1))    
    manhattan = Manhattan(dispatcher)
    manhattan.start(live=True)

if __name__ == "__main__":
    from sys import argv
    if len(argv) > 1:
        command_line_argument = argv[1]
        scenarios = {'1': scenario1, '2': scenario2, 
                     '3': scenario3, '4': scenario4,
                     '5': scenario5}
        if argv[1] in scenarios:
            manhattan = Manhattan(scenarios[argv[1]]())
            manhattan.start()            
        elif argv[1] == 'live':
            run_live_demo()
        else:
            print("Unrecognized demo: " + str(argv[1]))
    else:
        print('****************************************')
        print('ERROR: MISSING COMMAND LINE ARGUMENT')
        print('Usage: python dispatcher.py <SCENARIO>')
        print('Supported scenarios: 1, 2, 3, 4, 5, live')
        print('****************************************')


