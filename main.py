import sys
import os
import time
import threading

class Elevator:
    def __init__(self, numFloor=10, current_floor=0, moving=False, open=False, occupied=False, max_cap=100):
        super(Elevator, self).__init__()
        self.numFloor = numFloor
        self.current_floor = current_floor
        self.moving = moving
        self.open = open
        self.occupied = occupied
        self.max_capacity = max_cap

        self.queue = []
    def info(self):
        time.sleep(3)
        print('Num Floors:', self.numFloor)
        print('Current Floor:', self.current_floor)
        print('Status:',)
        if self.moving:
            print('Moving!')
        else:
            print('Waiting for call!')



class Event:
    def __init__(self, floor=0, up=0, timestamp=0):
        super(Event, self).__init__()
        self.floor = floor
        self.up = up
        self.timestamp = timestamp



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    elevator = Elevator()
    print('Elevator created!')

    # create thread to display elevator info regardless of user input
    threading1 = threading.Thread(target=elevator.info())
    threading1.daemon = True
    threading1.start()








