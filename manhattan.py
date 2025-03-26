from graphics import Window
from graphics import Rectangle, Circle, Textbox
from addresses import Address
from random import choice, uniform
from tasks import Delivery
from vehicles import Car, Vehicle, Van, Helicopter

CONFIG = {'block width': 50, 
          'road width': 25,
          'car width': 10,
          'van width': 15,
          'helicopter width': 15,
          'customer width': 21,
          'num rows': 8, 
          'num cols': 10,
          'time step': 4}


def draw_city_block(config):
    return Rectangle(config['block width'], 
                     config['block width'], 
                     fill_color="darkgray", 
                     outline_color="black")
     

def draw_vehicle(config, vehicle):
    if type(vehicle) == Car:
        return Rectangle(config['car width'],
                         config['car width'],
                         fill_color='gray' if vehicle.is_empty() else "blue",
                         outline_color='red' if vehicle.is_busy() else "green")
    elif type(vehicle) == Van:
        return Textbox(config['van width'],
                       config['van width'],
                       fill_color='gray' if vehicle.is_empty() else "blue",
                       text_color='white',
                       font_name='Helvetica',
                       msg = "V")
    elif type(vehicle) == Helicopter:
        return Circle(config['helicopter width'],
                      color='gray' if vehicle.is_empty() else "darkorange")
    else:
        return Circle(config['helicopter width'],
                      color='lightgray')

def draw_order(config, assigned):
    return Textbox(config['customer width'],
                   config['customer width'],
                   fill_color='green' if assigned else "yellow",
                   text_color='black',
                   font_name='Helvetica',
                   msg = "$")

def draw_warehouse(config):
    return Textbox(config['customer width'],
                   config['customer width'],
                   fill_color='blue',
                   text_color='white',
                   font_name='Helvetica',
                   msg = "W")


class Manhattan:

    def __init__(self, dispatcher, config=CONFIG):
        self.config = config
        self.dispatcher = dispatcher
        num_rows = config['num rows']
        num_cols = config['num cols']
        self.road_width = config['road width']
        block_width = config['block width']
        self.board_height = (num_rows * block_width) + (num_rows + 1) * self.road_width
        self.board_width = (num_cols * block_width) + (num_cols + 1) * self.road_width
        self.board = Window(self.board_width, self.board_height, "MANHATTAN", "white")    
        self.draw()
        
    def map_coords(self, x, y):
        new_x = (self.road_width // 2) + (x / 1000) * (self.board_width - self.road_width)
        new_y = (self.road_width // 2) + ((800 - y) / 800) * (self.board_height - self.road_width)
        return new_x, new_y

    def draw(self):
        self.board.clear()
        num_rows = self.config['num rows']
        num_cols = self.config['num cols']
        road_width = self.config['road width']
        block_width = self.config['block width']
        customer_width = self.config['customer width']
        for row in range(num_rows):
            for col in range(num_cols):
                brick = draw_city_block(self.config)
                self.board.paste(brick,
                                 road_width + col * (road_width + block_width),
                                 road_width + row * (road_width + block_width))
        for vehicle in self.dispatcher.fleet:
            x, y = self.map_coords(vehicle.curr_x, vehicle.curr_y)
            graphic = draw_vehicle(self.config, vehicle)
            if type(vehicle) == Van:
                vehicle_width = self.config['van width']
            elif type(vehicle) == Vehicle:
                vehicle_width = self.config['car width']
            else:
                vehicle_width = self.config['helicopter width']
            self.board.paste(graphic, x-vehicle_width//2, y-vehicle_width//2)
        offsets = {'NW': (32, -32), 'NE': (-32, -32),
                   'SW': (32, 32), 'SE': (-32, 32)}
        for warehouse in self.dispatcher.warehouses:
            addr_x, addr_y  = warehouse.get_coordinates()
            x, y = self.map_coords(addr_x + offsets[warehouse.corner][0], addr_y + offsets[warehouse.corner][1])
            graphic = draw_warehouse(self.config)
            self.board.paste(graphic, x-customer_width//2, y-customer_width//2)            
        for order in self.dispatcher.get_unfulfilled_orders():
            addr_x, addr_y  = order.address.get_coordinates()
            x, y = self.map_coords(addr_x + offsets[order.address.corner][0], addr_y + offsets[order.address.corner][1])
            graphic = draw_order(self.config, order.already_assigned())
            self.board.paste(graphic, x-customer_width//2, y-customer_width//2)            

    def advance_time(self):
        self.dispatcher.dispatch()
        if uniform(0, 50) < 1 and self.live:
            random_block = choice([str(i) for i in range(8)]) + choice([str(i) for i in range(10)])
            random_corner = choice(['NW', 'NE', 'SW', 'SE'])
            self.dispatcher.take_order(Delivery(Address(random_block, random_corner)))
      

    def start(self, live=False):
        self.live = live
        self.board.call_every_k_milliseconds(
            self.config['time step'],
            self.advance_time,
        )            
        quit_now = False
        while not quit_now:
            self.draw()
            quit_now = self.board.refresh()


