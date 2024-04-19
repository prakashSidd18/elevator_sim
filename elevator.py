import os
import sys
import time
from collections import deque

import events as e


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

    def reset(self):

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
            print('Failure 1! Wrong format!!')
            return False

        if int(call[0]) not in range(0, self.numFloor) or int(call[2]) not in range(0, self.numFloor):
            print('Failure 2! Floor out of range!!')
            return False

        if call[1] not in ['u', 'd']:
            print('Failure 3! Wrong format!!')
            return False

        if int(call[0]) == 0 and call[1] == 'd':
            print('Floor 0 can only go up!')
            return False

        if int(call[0]) == self.numFloor-1 and call[1] == 'u':
            print('Floor {} can only go down!'.format(self.numFloor-1))
            return False

        if call[1] == 'u' and int(call[0]) > int(call[2]):
            print('Call made to go up! Going down instead!!')
            return False

        if call[1] == 'd' and int(call[0]) < int(call[2]):
            print('Call made to go down! Going up instead!!')
            return False

        return True

    def schedule_calls(self, input_floors, timestamps):

        for idx, events in enumerate(input_floors):
            if not self.check_valid_call(events):
                print("Invalid call encountered: {}".format(events))
                sys.exit(-1)

            floor_call = int(events[0])
            direction = events[1]
            if direction == 'd':
                direction = 0
            else:
                direction = 1

            destination = int(events[2])
            current_ts = timestamps[idx]
            new_event = e.Event(floor=floor_call, up=direction, dst=destination, timestamp=current_ts)
            self.all_events.append(new_event)

        # self.display_queue()
        print('All calls valid! Run elevator!!')

    def run_elevator(self):
        if len(self.all_events) == 0:
            print('No calls made!!')
            return

        order = []
        print('Elevator Running....')
        self.log_time()

        time_to_reach_next = 0.0
        next_event_id = 0
        num_events_total = len(self.all_events)
        current_event = None
        while True:
            time_elapsed = time.time() - self.start_time
            print('Time elapsed {:2f} sec....'.format(time_elapsed), end='\r')

            # Keep checking when new calls are made
            # [TODO: multi-threading] should be done on a separate thread in a thread-safe manner
            if next_event_id < num_events_total:
                next_event_available_ts = self.all_events[next_event_id].timestamp
                # if next event occurred at current time stamp, make it available from the queue
                if next_event_available_ts - time_elapsed <= 0.0001:
                    # make it available
                    self.call_queue.append(self.all_events[next_event_id])
                    self.all_events[next_event_id].display(message='* Call made')
                    self.rearrange_call_queue()
                    next_event_id += 1

            # if call queue has elements, execute the next call in queue
            if len(self.call_queue) > 0:
                current_event = self.call_queue[0]
                if not self.moving:
                    # self.display_queue(self.call_queue)
                    time_to_reach_next = self.set_next_floor(current_event.floor, time_elapsed)
                else:
                    # [TODO] update current floor while elevator moving to keep track of nearby floors

                    # elevator reached next floor and waiting to take passengers
                    if (time_to_reach_next - time_elapsed) <= 0.0001:
                        order.append(current_event.floor)
                        print('[Visited] floor ', current_event.floor, end='\t')
                        print('at time: {:2f} sec....'.format(time_elapsed))
                        self.current_floor = current_event.floor
                        dest_floor = current_event.dst

                        self.call_queue.popleft()

                        # insert the destination for current event and reorder queue
                        # take ALL available event into account
                        # based on inserted event to prioritize nearby on-way floors
                        if dest_floor != -1:
                            # remains static at floor reached for given seconds
                            print('Waiting to Board...')
                            time.sleep(self.static)
                            print('(Boarded) at floor {}!'.format(self.current_floor))
                            print('(Destination) entered to floor {}!'.format(dest_floor))
                            self.insert_destination(dest_floor, time_elapsed)
                        else:
                            # remains static at floor reached for given seconds
                            print('Waiting to De-board...')
                            time.sleep(self.static)
                            print('(De-Boarded) at floor {}!'.format(self.current_floor))

                        self.rearrange_call_queue()
                        self.moving = False

            elif next_event_id == num_events_total:
                break

        # all floors scheduled and called
        print('Simulation done!')
        print('Order of floors visited:')
        self.display_floors_visited(order)

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
        new_event = e.Event(floor=dst, up=direction, dst=-1, timestamp=time_elapsed, called=True)
        self.dest_queue.append(new_event)

        return

    def rearrange_call_queue(self):
        priority_dest = None
        # create a map of all events which come on-way of destination
        # and store its distance from current destination to prioritize
        valid_event_distance = {}
        # else put all other events in a list
        invalid_events = []
        priority_call = False
        while len(self.dest_queue) > 0:
            dest_present = False
            priority_call = True
            priority_dest = self.dest_queue[0]
            self.dest_queue.popleft()
            # print('###Destination queue dequeued floor {}!'.format(priority_dest.floor))

            # iterate through events already in call queue
            for scheduled_events in self.call_queue:
                # if call to destination already exists in queue
                if scheduled_events.floor == priority_dest.floor and scheduled_events.up == priority_dest.up:
                    dest_present = True
                    valid_event_distance[scheduled_events] = abs(self.current_floor - scheduled_events.floor)

                # check which events are on-way of destination and add it to the final queue
                if self.current_floor < priority_dest.floor:
                    floor_range = list(range(self.current_floor, priority_dest.floor))
                else:
                    floor_range = list(range(self.current_floor, priority_dest.floor, -1))

                if (scheduled_events.floor in floor_range) and scheduled_events.up == priority_dest.up:
                    valid_event_distance[scheduled_events] = abs(self.current_floor - scheduled_events.floor)
                else:
                    invalid_events.append(scheduled_events)

            # finally add the destination if not already present in queue with its distance from current floor
            if not dest_present:
                valid_event_distance[priority_dest] = abs(self.current_floor - priority_dest.floor)

        # if destination queue is empty and elevator stopped at a floor (to de-board),
        # check if current floor in queue and prioritize it
        if not priority_call and not self.moving:
            # iterate through events already in call queue
            for scheduled_events in self.call_queue:
                # check if current floor in queue to board
                if scheduled_events.floor == self.current_floor:
                    valid_event_distance[scheduled_events] = abs(self.current_floor - scheduled_events.floor)
                else:
                    invalid_events.append(scheduled_events)
        else:
            # a new call was inserted; check if elevator is nearby
            # re-organize the queue to take new event into account while moving
            for scheduled_events in self.call_queue:
                valid_event_distance[scheduled_events] = abs(self.current_floor - scheduled_events.floor)
            self.moving = False

        temp_queue = deque()

        for key, value in sorted(valid_event_distance.items(), key=lambda item: item[1]):
            temp_queue.append(key)

        for scheduled_events in invalid_events:
            temp_queue.append(scheduled_events)

        self.call_queue = temp_queue
        # self.display_queue(self.call_queue)
        return

    def display_queue(self, queue):
        print('***************************************')
        for id, event in enumerate(queue):
            event.display(message='! Disp ')
        print('***************************************')

    def log_time(self):
        self.start_time = time.time()

    def display_floors_visited(self, order):
        prev_floor = -1
        for floor in order:
            if not floor == prev_floor:
                print('{}->'.format(floor), end='')
                prev_floor = floor
        print('fin!')

