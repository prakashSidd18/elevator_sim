import sys
import time
from collections import deque


class Event:
    def __init__(self, floor=0, up=0, dst=0, timestamp=0.0):
        super(Event, self).__init__()
        self.floor = floor
        self.up = up
        self.dst = dst
        self.timestamp = timestamp

    def display(self):
        direction = "dn"
        if self.up:
            direction = "up"
        print('* Call made at floor {} going {} at time: {} secs.'.format(
            self.floor, direction, self.timestamp))


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
        self.static = 5

        self.start_time = 0.0
        self.end_time = 0.0

        self.all_events = deque()
        self.call_queue = deque()
        self.dest_queue = deque()

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
            self.all_events.append(new_event)
            time_bn_calls += 3

        # self.display_queue()
        print('All calls valid! Run elevator!!')

    def run_elevator(self):
        if len(self.all_events) == 0:
            print('No calls made!!')
            return

        order = []
        print('Elevator Running....', end='\r')
        self.log_time()

        time_to_reach_next = 0.0
        next_event_id = 0
        num_events_total = len(self.all_events)

        while True:
            time_elapsed = time.time() - self.start_time
            print('Time elapsed {:2f} sec....'.format(time_elapsed), end='\r')

            if next_event_id < num_events_total:
                next_event_available_ts = self.all_events[next_event_id].timestamp
            # if next event occurred at current time stamp, make it available from the queue
            if next_event_id < num_events_total and (next_event_available_ts - time_elapsed) <= 0.0001:
                # make it available
                self.call_queue.append(self.all_events[next_event_id])
                self.all_events[next_event_id].display()
                next_event_id += 1

            if len(self.call_queue) > 0:
                current_event = self.call_queue[0]

                if not self.moving:
                    time_to_reach_next = self.set_next_floor(current_event.floor, time_elapsed)
                else:
                    # elevator reached next floor and waiting to take passengers
                    if (time_to_reach_next - time_elapsed) <= 0.0001:
                        order.append(current_event.floor)
                        print('[Visited floor] ', current_event.floor, end='\t')
                        print('at time: {:2f} sec....'.format(time_elapsed))
                        self.current_floor = current_event.floor
                        dest_floor = current_event.dst
                        # remains static at floor reached for given seconds
                        time.sleep(self.static)
                        self.call_queue.popleft()

                        # insert the destination for current event as priority and reorder queue
                        if current_event.dst != -1:
                            self.insert_destination(dest_floor, time_elapsed)

                        self.moving = False

                        # time_to_reach_next = self.set_next_floor(current_event.dst, time_elapsed)
            elif next_event_id == num_events_total:
                break

        # all floors scheduled and called
        print('Simulation done!')
        print('Order of floors visited:', order)

    def set_next_floor(self, floor, time_elapsed):
        self.dest_floor = floor
        self.moving = True
        time_to_reach_next = time_elapsed + (abs(self.current_floor - self.dest_floor) * self.speed)
        return time_to_reach_next

    def insert_destination(self, dst, time_elapsed):
        if self.current_floor - dst > 0:
            direction = 0
        else:
            direction = 1
        new_event = Event(floor=dst, up=direction, dst=-1, timestamp=time_elapsed)
        self.dest_queue.append(new_event)
        self.rearrange_call_queue()

        return

    def rearrange_call_queue(self):
        priority_dest = None

        # create a map of all events which come in way and store its distance from current destination to prioritize
        valid_event_distance = {}
        invalid_events = []
        if len(self.dest_queue) > 0:
            priority_dest = self.dest_queue[0]
            self.dest_queue.popleft()

            # check which events are on-way of destination and add it to the final queue
            for events in self.call_queue:
                direction = priority_dest.up
                if events.floor in range(self.current_floor, self.dest_floor) and events.up == direction:
                    valid_event_distance[events] = abs(self.current_floor - events.floor)
                else:
                    invalid_events.append(events)

        temp_queue = deque()
        if priority_dest:
            temp_queue.append(priority_dest)

        for key, value in sorted(valid_event_distance.items(), key=lambda item: item[1]):
            temp_queue.append(key)

        for events in invalid_events:
            temp_queue.append(events)

        self.call_queue = temp_queue

        return

    def display_queue(self):
        for id, event in enumerate(self.call_queue):
            event.display()

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






