MaxCapacity = 13
import time


class Elevator:
    """constructor"""

    def __init__(self, id, floor=1):
        self.floor = floor
        self.id = id
        self.people = []
        self.doortime = 0.15
        self.traveltime = 0.03
        self.direction = 'idle'  # or 'up' or 'down'
        self.listOfLoads = []
        self.listOfUnloads = []
        self.timeTraveled = 0

    def getTimeTraveled(self):
        return self.timeTraveled

    def getFloor(self):
        return self.floor

    def getID(self):
        return self.id

    def elevatorIsDown(self, floor):
        for i in self.listOfUnloads:
            if floor > i:
                return False
        return True

    def elevatorIsUp(self, floor):
        for i in self.listOfUnloads:
            if floor < i:
                return False
        return True

    def hasMoreStops(self):
        if len(self.listOfUnloads) != 0:
            return True
        else:
            return False

    """how much floors elevator should pass"""

    def request(self, floor):
        if self.floor == floor:
            return 0
        if len(self.people) > 0:
            return 100
        return abs(floor - self.floor)  # return how much floors the elevator should pass

    def step(self, inFloor):

        print 'BEST ELEVATOR:\n', self.__repr__()

        if self.direction == 'up':
            if len(self.listOfUnloads) + len(inFloor.getUps()) > MaxCapacity:
                while (len(self.listOfUnloads) + len(inFloor.getUps()) < MaxCapacity):
                    if len(inFloor.getUps()) != 0:
                        print "UPS 111 = ", inFloor.getUps()
                        self.listOfUnloads.append(inFloor.getUps().pop(0))
                        print "UPS 222 = ", inFloor.getUps()
                    else:
                        break

            else:
                self.listOfUnloads.extend(inFloor.getUps())

            self.listOfLoads.sort()
            self.listOfUnloads.sort()
        else:
            if len(self.listOfUnloads) + len(inFloor.getDowns()) > MaxCapacity:
                while (len(self.listOfUnloads) + len(inFloor.getDowns()) < MaxCapacity):
                    if len(inFloor.getDowns()) != 0:
                        print "Downs 111 = ", inFloor.getDowns()
                        self.listOfUnloads.append(inFloor.getDowns().pop(0))
                        print "Downs 222 = ", inFloor.getDowns()
                    else:
                        break
            else:
                self.listOfUnloads.extend(inFloor.getDowns())

            self.listOfLoads.sort(reverse=True)
            self.listOfUnloads.sort(reverse=True)

        print "list of Ups 11111 ", self.listOfLoads, "List of Downs 11111 ", self.listOfUnloads

        while self.floor not in (self.listOfLoads or self.listOfUnloads):
            if (self.direction == 'up'):
                self.floor += 1
            elif (self.direction == 'down'):
                self.floor -= 1
            self.timeTraveled += self.traveltime
            time.sleep(self.traveltime)
        print "list of Ups 22222 ", self.listOfLoads, "List of Downs 22222 ", self.listOfUnloads

        if self.floor in self.listOfLoads:
            self.listOfLoads = [x for x in self.listOfLoads if x != self.floor]
            self.timeTraveled += self.doortime
            time.sleep(self.doortime)
            print 'Deleted from list of loads', self.floor

        if self.floor in self.listOfUnloads:
            self.listOfUnloads = [x for x in self.listOfUnloads if x != self.floor]
            self.timeTraveled += self.doortime
            time.sleep(self.doortime)
            print 'Deleted from list of unloads', self.floor

        if len(self.listOfLoads) == 0 and len(self.listOfUnloads) == 0:
            self.direction = 'idle'

    def endStep(self):

        """handle situation: if There are no orders but there are people in the elevator, and elevator is idle"""
        while self.floor not in (self.listOfLoads or self.listOfUnloads):
            if (self.direction == 'up'):
                self.floor += 1
            elif (self.direction == 'down'):
                self.floor -= 1
            else:
                if self.elevatorIsDown(self.floor):
                    self.direction = 'up'
                    self.floor += 1
                elif self.elevatorIsUp(self.floor):
                    self.direction = 'down'
                    self.floor -= 1

            self.timeTraveled += self.traveltime
            time.sleep(self.traveltime)

        if self.floor in self.listOfUnloads:
            self.listOfUnloads = [x for x in self.listOfUnloads if x != self.floor]
            self.timeTraveled += self.doortime
            time.sleep(self.doortime)
            print 'Deleted from list of unloads', self.floor

        if len(self.listOfUnloads) == 0:
            self.direction = 'idle'


    def addToLoads(self, floor):
        return self.listOfLoads.append(floor)

    def addToUnloads(self, floor):
        return self.listOfUnloads.append(floor)

    def removeStop(self):
        if len(self.listOfLoads) != 0:
            self.listOfLoads.pop(0)
        else:
            return 'List of stops is empty.'

    def status(self):
        if self.direction == 'idle': return 'idle'
        if self.direction == 'up': return 'up'
        if self.direction == 'down': return 'down'

    def up(self, floors):
        self.floor += floors
        self.direction = 'up'

    def down(self, floors):
        self.floor -= floors
        self.direction = 'down'

    def setDirection(self, dir):
        self.direction = dir

    def busy(self):
        if self.direction == 'up' or self.direction == 'down':
            return True
        else:
            return False

            # def elevate(self, group, requestingFloor, floorSet):
            #     waitTime = self.traveltime * abs(self.floor - requestingFloor)
            #     waitTime += self.doortime

    def __repr__(self):
        return '\nElevator(ID = {}):\nfloor = {}\nPeople = {}\nDirection = {}\nLoads = {}\nUnloads = {}\n'.format(
            self.id, self.floor,
            self.people,
            self.direction,
            self.listOfLoads, self.listOfUnloads)
