from pgl import GWindow, GCompound, GOval, GRect, GLine, GLabel
from lab8 import Dispatcher, Van, Location, Warehouse, Vehicle
from random import randint

GWINDOW_WIDTH = 500
GWINDOW_HEIGHT = 500

CAR_RADIUS = 10
HOUSE_RADIUS = 5
CUSTOMER_RADIUS = 8

TIME_STEP = 500

def draw_van(center_x, center_y, radius, van):
    result = GCompound()
    oval = GOval(center_x - radius, center_y - radius, radius*2, radius*2)
    result.add(oval)
    oval.setFilled(True)
    oval.setColor("red")
    try:
        if van.is_available():
            oval.setColor("green")
        else:
            oval.setColor("red")
        label = GLabel(str(van.get_cargo()))
        result.add(label, center_x - label.getWidth() // 2, center_y + label.getAscent() // 2 - 2)
    except:
        pass
    return result


def simple_square(center_x, center_y, radius):
    return GRect(center_x - radius, center_y - radius, radius*2, radius*2)

def double_ring(center_x, center_y, radius, scheduled):
    result = GCompound()
    outer = GRect(center_x - radius, center_y - radius, radius*2, radius*2)
    inner = GOval(center_x - radius//2, center_y - radius//2, radius, radius)
    outer.setColor("blue")
    inner.setColor("blue")
    result.add(outer)
    result.add(inner)
    if scheduled:
        inner.setFilled(True)
    return result


class Grid:

    def __init__(self, num_rows):
        self.num_rows = num_rows
        self.vans = []
        self.warehouses = []
        self.customers = []

    def add_van(self, van):
        self.vans += [van]

    def add_warehouse(self, warehouse):
        self.warehouses += [warehouse]

    def add_customer(self, row, col, scheduled=False):
        self.customers += [(row, col, scheduled)]

    def get_coords(self, row, col):
        x = -200 + (400 / self.num_rows) * row
        y = 200 - (400 / self.num_rows) * col
        return (x, y)

    def gcompound(self):
        result = GCompound()
        for i in range(self.num_rows+1):
            offset = (i - (self.num_rows / 2)) * (400 / self.num_rows)
            x_axis = GLine(-200, offset, 200, offset)
            result.add(x_axis)
            y_axis = GLine(offset, -200, offset, 200)
            result.add(y_axis)
        for van in self.vans:
            (x, y) = self.get_coords(van.get_location().x, van.get_location().y)
            car = draw_van(x, y, CAR_RADIUS, van)
            result.add(car)
        for wh in self.warehouses:
            (x, y) = self.get_coords(wh.get_location().x, wh.get_location().y)
            house = simple_square(x, y, HOUSE_RADIUS)
            house.setFilled(True)
            house.setColor("black")
            result.add(house)
        for (row, col, scheduled) in self.customers:
            (x, y) = self.get_coords(row, col)
            house = double_ring(x, y, CUSTOMER_RADIUS, scheduled)
            result.add(house)
        return result




def create_grid(dispatcher):
    grid = Grid(10)
    for warehouse in dispatcher.warehouses:
        grid.add_warehouse(warehouse)
    for van in dispatcher.fleet:
        grid.add_van(van)
        try:
            if van.get_current_task() == "deliver" and van.get_destination() != None:
                destination = van.get_destination()
                grid.add_customer(destination.x, destination.y, True)
        except:
            pass
    for destination in dispatcher.unfilled:
        grid.add_customer(destination.x, destination.y)
    return grid

class EasyDispatcher:

    def __init__(self, warehouses=[]):
        self.warehouses = warehouses
        self.fleet = []
        self.unfilled = []

    def hire(self, vehicle):
        self.fleet += [vehicle]

    def advance_time(self):
        for van in self.fleet:
            van.advance_time()







def start_scenario1():
    def step():
        gw.clear()
        grid = create_grid(dispatcher)
        gw.add(grid.gcompound(), GWINDOW_WIDTH // 2, GWINDOW_HEIGHT // 2)
        car.advance_time()

    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    car = Vehicle(Location(1, 4))
    car.set_destination(Location(8, 10))
    dispatcher = EasyDispatcher()
    dispatcher.hire(car)
    timer = gw.setInterval(step, TIME_STEP)
    timer.setRepeats(True)


def start_scenario2():
    def step():
        gw.clear()
        grid = create_grid(dispatcher)
        gw.add(grid.gcompound(), GWINDOW_WIDTH // 2, GWINDOW_HEIGHT // 2)
        van.advance_time()
        van.deliver()

    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    van = Van(3)
    van.schedule(Location(5, 3), "deliver")
    dispatcher = EasyDispatcher()
    dispatcher.hire(van)
    timer = gw.setInterval(step, TIME_STEP)
    timer.setRepeats(True)


def start_scenario3():
    def step():
        gw.clear()
        grid = create_grid(dispatcher)
        gw.add(grid.gcompound(), GWINDOW_WIDTH // 2, GWINDOW_HEIGHT // 2)
        van.advance_time()
        if warehouse.refill(van):
            van.set_destination(Location(10, 10))

    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    van = Van(5)
    van.dump_cargo()
    van.schedule(Location(6, 4), "refill")
    warehouse = Warehouse(Location(6, 4))
    dispatcher = EasyDispatcher([warehouse])
    dispatcher.hire(van)
    timer = gw.setInterval(step, TIME_STEP)
    timer.setRepeats(True)


def start_final_scenario():
    def step():
        gw.clear()
        grid = create_grid(dispatcher)
        gw.add(grid.gcompound(), GWINDOW_WIDTH // 2, GWINDOW_HEIGHT // 2)
        dispatcher.advance_time()
        if randint(1,3) == 1:
            dispatcher.take_order(Location(randint(0,10), randint(0,10)))

    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    dispatcher = Dispatcher([Warehouse(Location(5, 5)), Warehouse(Location(2, 9))])
    dispatcher.hire(Van(3))
    dispatcher.hire(Van(3))
    dispatcher.hire(Van(3))
    dispatcher.take_order(Location(9, 7))
    timer = gw.setInterval(step, TIME_STEP)
    timer.setRepeats(True)




if __name__ == '__main__':
    import sys
    failed = False
    if len(sys.argv) < 1:
        failed = True
    elif sys.argv[1] == "vehicles":
        start_scenario1()
    elif sys.argv[1] == "vans":
        start_scenario2()
    elif sys.argv[1] == "warehouses":
        start_scenario3()
    elif sys.argv[1] == "dispatcher":
        start_final_scenario()
    else:
        failed = True
    if failed:
        print("Supported scenarios: vehicles, vans, warehouses, dispatcher")




