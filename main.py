import sys
import os
import time
import threading
from collections import deque



class Event:
    def __init__(self, floor=0, up=0, dst=0, timestamp=0.0):
        super(Event, self).__init__()
        self.floor = floor
        self.up = up
        self.dst = dst
        self.timestamp = timestamp

    def display(self, id):
        dir = "down"
        if self.up:
            dir = "up"
        print('{}. Call made at floor {} going {} to destination {} at time {}'.format(
            id, self.floor, dir, self.dst, self.timestamp))

class Elevator:
    def __init__(self, numFloor=10, current_floor=0, moving=False, open=False, occupied=False, max_cap=100):
        super(Elevator, self).__init__()
        self.numFloor = numFloor
        self.current_floor = current_floor
        self.dest_floor = 0
        self.moving = moving
        self.open = open
        self.occupied = occupied
        self.max_capacity = max_cap

        # assume 1 second to move 1 floor
        self.speed = 1.0

        # assume remains static at a floor for 2 secs. and user inputs the next call within this time
        self.static = 2.0

        self.start_time = 0.0
        self.end_time = 0.0

        self.queue = deque()

    def info(self):
        print('Num Floors:', self.numFloor)
        print('Current Floor:', self.current_floor)
        print('Status:',end='\t')
        if self.moving:
            print('Moving!')
        else:
            print('Waiting for call!')

    def check_valid_call(self, call):
        if len(call) != 3:
            print('Failure 1')
            return False

        if int(call[0]) not in range(0, self.numFloor) or int(call[2]) not in range(0, self.numFloor):
            print('Failure 2')
            return False

        if call[1] not in ['u', 'd']:
            print('Failure 3')
            return False

        if int(call[0]) == 0 and call[1] == 'd':
            print('Floor 0 can only go up!')
            return False

        if int(call[0]) == self.numFloor-1 and call[1] == 'u':
            print('Floor {} can only go up!'.format(self.numFloor-1))
            return False

        return True

    def schedule_calls(self, input_floors):
        time_bn_calls = 0
        for id, events in enumerate(input_floors):
            if not self.check_valid_call(events):
                print("Invalid call encountered: {}".format(events))
                sys.exit(-1)

            floor_call = int(events[0])
            direction  = events[1]
            if direction == 'd':
                direction = 0
            else:
                direction = 1
            destination= int(events[2])
            current_ts = time_bn_calls
            new_event = Event(floor=floor_call, up=direction, dst=destination, timestamp=current_ts)
            self.queue.append(new_event)
            time_bn_calls += 3

        self.display_queue()
        print('All calls valid! Run elevator!!')

    def run_elevator(self):
        if len(self.queue) == 0:
            print('No calls made!!')
            return

        order = []
        print('Elevator Running....', end='\r')
        self.log_time()
        next_event = None
        time_to_reach_next = 0.0
        current_event = self.queue[0]
        while current_event is not None:
            time_elapsed = time.time() - self.start_time
            print('Time elapsed {:2f} sec....'.format(time_elapsed), end='\r')
            if len(self.queue) > 1:
                next_event = self.queue[1]
            else:
                next_event = None

            numEvents = len(self.queue)

            if not self.moving:
                time_to_reach_next = self.set_next_floor(current_event.floor, time_elapsed)

            # if next event occured before elevator reached it's destination
            # if (next_event.timestamp - time_elapsed) <= 0.01:
            #     # add to the queue
            #     pass

            # elevator reached next floor and waiting to take passengers
            if (time_to_reach_next - time_elapsed) <= 0.01:
                order.append(current_event.floor)
                print('Visited floor: ', current_event.floor)
                self.current_floor = current_event.floor

                # remains static at floor reached for given seconds
                time.sleep(self.static)
                self.queue.popleft()
                self.moving = False
                # time_to_reach_next = self.set_next_floor(current_event.dst, time_elapsed)
                current_event = next_event



        # if all floors scheduled and called
        print('Simulation done!')
        print('Order of floors visited:', order)

    def set_next_floor(self, floor, time_elapsed):
        self.dest_floor = floor
        self.moving = True
        time_to_reach_next = time_elapsed + (abs(self.current_floor - self.dest_floor) * self.speed)
        return time_to_reach_next

    def display_queue(self):
        for id, event in enumerate(self.queue):
            event.display(id)

    def log_time(self):
        self.start_time = time.time()


if __name__ == '__main__':
    elevator = Elevator()
    print('Elevator created!')
    elevator.info()
    print('***************************************')

    # provide the elevator call events for simulation
    # format: <floor_called><direction><destination_floor>
    # ex: "4u6" means elevator called on floor 4, to go up, with destination floor 6
    input_floors = ["4u6", "3d0", "0u9", "5u7", "3d2", "4u9", "9d2"]

    elevator.schedule_calls(input_floors)

    elevator.run_elevator()






