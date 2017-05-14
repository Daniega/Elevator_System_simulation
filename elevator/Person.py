import random

class Person:
    """constructor"""

    def __init__(self, floor, numOfFloors):
        self.floor = floor
        n = floor
        r = range(1, n) + range(n + 1, numOfFloors + 1)
        self.desiredFloor = random.choice(r)
        self._wait = 0
        self.arrived = False

    def direction(self):
        if self.floor < self.desiredFloor:
            return 'up'
        else:
            return 'down'

    def getFloor(self):
        return self.floor

    def destintaion(self):
        return self.desiredFloor

    def wait(self, number):
        self._wait += number

    def __repr__(self):
        return 'Person(floor = {}, going to = {})'.format(self.floor, self.desiredFloor)
