class Event:
    def __init__(self, floor=0, up=0, dst=0, timestamp=0.0):
        super(Event, self).__init__()
        self.floor = floor
        self.up = up
        self.dst = dst
        self.timestamp = timestamp

    def display(self, message='?'):
        direction = "dn"
        if self.up:
            direction = "up"
        print('{} at floor {} going {} at time: {} secs.'.format(message, self.floor, direction, self.timestamp))
