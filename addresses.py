class Address:

    def __init__(self, block_id, corner):
        self.block_id = block_id
        self.corner = corner
        """Replace this with your code for Question One ("Addresses")."""
        
    def get_coordinates(self):
        """Replace this with your code for Question One ("Addresses")."""
    
    def __eq__(self, loc):
        if type(loc) != Address:
            return False
        else:          
            return self.block_id == loc.block_id and self.corner == loc.corner

    def __repr__(self):
        return 'Address("' + self.block_id + '", "' + self.corner + '")'


