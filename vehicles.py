from oscar import direct_path

class Vehicle:

    def __init__(self, starting_address, speed):
        self.speed = speed

    def get_coordinates(self):
        """Replace this with your code for Question Two ("Vehicles")."""

    def get_eta(self, addr):
        """Replace this with your code for Question Two ("Vehicles")."""
    
    def send_to(self, addr):
        """Replace this with your code for Question Two ("Vehicles")."""

    def is_busy(self):
        """Replace this with your code for Question Two ("Vehicles")."""

    def is_empty(self):
        """Replace this with your code for Question Two ("Vehicles")."""

    def refill(self):
        """Replace this with your code for Question Two ("Vehicles")."""

    def deliver(self):
        """Replace this with your code for Question Two ("Vehicles")."""
        
    def move(self):
        """Replace this with your code for Question Two ("Vehicles")."""
               

class Car(Vehicle):
    """This class is written for you. Do not modify it."""
    def __init__(self, starting_address):
        super().__init__(starting_address, 2)


class Van(Vehicle):
    """Replace this with your code for Question Four ("Vans")."""


class Helicopter(Vehicle):
    """Replace this with your code for Question Five ("Helicopters")."""

    