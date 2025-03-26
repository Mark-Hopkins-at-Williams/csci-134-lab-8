class Task:

    def __init__(self, address):
        self.address = address
        self.assignee = None

    def can_be_assigned_to(self, vehicle):
        return not vehicle.is_busy()

    def assign_to(self, vehicle):
        self.assignee = vehicle

    def already_assigned(self):
        return self.assignee != None
    
    def attempt(self):
        return False
    

class Delivery(Task):
    """Replace this with your code for Question Three ("Tasks")."""


class Refill(Task):
    """Replace this with your code for Question Three ("Tasks")."""
