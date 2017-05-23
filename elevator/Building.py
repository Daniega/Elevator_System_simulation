import time
import threading
import random

from Floor import Floor
from Elevator import Elevator
from Person import Person


class Building:
    elevators = []
    threads = []
    elevatorCalls = []
    totalTravelTime = 0
    peopleInFloors = []
    answer = 0

    """constructor"""

    def __init__(self, numberOfPeople, numOfFloors, numOfElevators):

        self.numberOfPeople = numberOfPeople
        self.numberOfFloors = numOfFloors
        self.floors = {}
        self.elevators = []

        peopleInFloor = int(numberOfPeople / numOfFloors)
        """need to fix"""
        # peopleInFloor = int(numberOfPeople / numOfFloors)
        # if peopleInFloor < 1:
        #     while i < numberOfPeople:
        #         rand = random.randint(0, 1)
        #         if rand == 1:
        #             while floorNum < numOfFloors + 1:
        #                 self.floors[floorNum] = Floor(floorNum, rand, numOfFloors)
        #                 floorNum += 1
        #         else:

        for floorNum in range(1, numOfFloors + 1):
            self.floors[floorNum] = Floor(floorNum, peopleInFloor, numOfFloors)

        for i in range(0, numOfElevators):
            self.elevators.append(Elevator(i, numOfFloors))

            # print self.elevators
            # print 'Floors: ', self.floors

    def floorCheck(self):
        for k, v in self.floors.items():
            if v.isNotEmpty():
                return False
        return True

    def elevatorCheck(self):
        for ele in self.elevators:
            if ele.hasMoreStops():
                return False
        return True

    def optimalElevatorID(self, source, direction):
        elevatorFloors = {}

        print self.elevators
        for elevator in self.elevators:

            if elevator.getFloor() < source and (elevator.status() == 'up' and source == 'up'):
                elevatorFloors[elevator.getID()] = abs(elevator.getFloor() - source)

            elif elevator.getFloor() > source and (elevator.status() == 'down' and source == 'down'):
                elevatorFloors[elevator.getID()] = abs(elevator.getFloor() - source)

            elif elevator.status() == 'idle':
                elevatorFloors[elevator.getID()] = abs(elevator.getFloor() - source)

        print 'elevatorFloors = ', elevatorFloors
        if len(elevatorFloors) != 0:
            optimal = min(elevatorFloors.items(), key=lambda x: x[1])
            if self.elevators[optimal[0]].getFloor() < source and direction == 'down':
                self.elevators[optimal[0]].setDirection('up')
            elif self.elevators[optimal[0]].getFloor() > source and direction == 'up':
                self.elevators[optimal[0]].setDirection('down')
            else:
                self.elevators[optimal[0]].setDirection(direction)

            return optimal[0]

        return -1

    """Regular simulation, when elevator finishes unloading, stays in current floor"""

    def simulateStrategy1(self):
        t = {}

        """Iterate until all people get to their destination (all people drom all floors get to elevator)"""
        while (self.floorCheck() == False):
            """Get random floor, so call to elevator will be from random floor"""
            randFloor = random.randint(1, self.numberOfFloors)
            if not self.floors[randFloor].isEmpty():  # if random floor is not empty, get random person from this floor
                person = self.floors[randFloor].getPerson()

                """check person destination and add to floors UPS/DOWNS list"""
                if person.direction == 'up':
                    self.floors[randFloor].addUp(person.destintaion())
                else:
                    self.floors[randFloor].addDown(person.destintaion())

                print 'Source = ', person.getFloor(), 'Destination = ', person.destintaion(), 'Direction = ', person.direction()
                bestElevator = self.optimalElevatorID(person.floor, person.direction()) # Choose best elevator to collect person
                if bestElevator != -1: # If there is a best elevator?
                    print 'bestElevator = ', bestElevator
                    self.elevators[bestElevator].addToLoads(person.getFloor()) # Add persons floor to elevators 'Loads' list
                    t[bestElevator] = threading.Thread(target=self.elevators[bestElevator].step(self.floors[randFloor])) # Thread of elevator
                    if not t[bestElevator].isAlive():
                        t[bestElevator].start()
                        print  t[bestElevator]

                    randTime = random.uniform(0.1, 1.0)
                    time.sleep(randTime)
                else:
                    self.floors[randFloor].pushPerson(person) # If there is no best elevator, person should wait until there is a best elevator
        for thread in t:
            t[thread].join()

        while (self.elevatorCheck() == False):
            for ele in self.elevators:
                if (ele.hasMoreStops()):
                    t[ele.getID()] = threading.Thread(target=self.elevators[ele.getID()].endStep())
                    t[ele.getID()].start()
        for thread in t:
            t[thread].join()

        for ele in self.elevators:
            self.totalTravelTime += ele.getTimeTraveled()
        answer = self.totalTravelTime / self.numberOfPeople
        return answer

    def simulateStrategy2(self):
        t = {}

        """Iterate until all people get to their destination (all people drom all floors get to elevator)"""
        while (self.floorCheck() == False):
            """Get random floor, so call to elevator will be from random floor"""
            randFloor = random.randint(1, self.numberOfFloors)
            if not self.floors[randFloor].isEmpty():  # if random floor is not empty, get random person from this floor
                person = self.floors[randFloor].getPerson()

                """check person destination and add to floors UPS/DOWNS list"""
                if person.direction == 'up':
                    self.floors[randFloor].addUp(person.destintaion())
                else:
                    self.floors[randFloor].addDown(person.destintaion())

                print 'Source = ', person.getFloor(), 'Destination = ', person.destintaion(), 'Direction = ', person.direction()
                bestElevator = self.optimalElevatorID(person.floor, person.direction()) # Choose best elevator to collect person
                if bestElevator != -1: # If there is a best elevator?
                    print 'bestElevator = ', bestElevator
                    self.elevators[bestElevator].addToLoads(person.getFloor()) # Add persons floor to elevators 'Loads' list
                    t[bestElevator] = threading.Thread(target=self.elevators[bestElevator].step2(self.floors[randFloor])) # Thread of elevator
                    if not t[bestElevator].isAlive():
                        t[bestElevator].start()
                        print  t[bestElevator]

                    randTime = random.uniform(0.1, 1.0)
                    time.sleep(randTime)
                else:
                    self.floors[randFloor].pushPerson(person) # If there is no best elevator, person should wait until there is a best elevator
        for thread in t:
            t[thread].join()

        while (self.elevatorCheck() == False):
            for ele in self.elevators:
                if (ele.hasMoreStops()):
                    t[ele.getID()] = threading.Thread(target=self.elevators[ele.getID()].endStep())
                    t[ele.getID()].start()
        for thread in t:
            t[thread].join()

        for ele in self.elevators:
            self.totalTravelTime += ele.getTimeTraveled()
        answer = self.totalTravelTime / self.numberOfPeople
        return answer


    def simulateStrategy3(self):
        t = {}

        """Iterate until all people get to their destination (all people drom all floors get to elevator)"""
        while (self.floorCheck() == False):
            """Get random floor, so call to elevator will be from random floor"""
            randFloor = random.randint(1, self.numberOfFloors)
            if not self.floors[randFloor].isEmpty():  # if random floor is not empty, get random person from this floor
                person = self.floors[randFloor].getPerson()

                """check person destination and add to floors UPS/DOWNS list"""
                if person.direction == 'up':
                    self.floors[randFloor].addUp(person.destintaion())
                else:
                    self.floors[randFloor].addDown(person.destintaion())

                print 'Source = ', person.getFloor(), 'Destination = ', person.destintaion(), 'Direction = ', person.direction()
                bestElevator = self.optimalElevatorID(person.floor, person.direction()) # Choose best elevator to collect person
                if bestElevator != -1: # If there is a best elevator?
                    print 'bestElevator = ', bestElevator
                    self.elevators[bestElevator].addToLoads(person.getFloor()) # Add persons floor to elevators 'Loads' list
                    t[bestElevator] = threading.Thread(target=self.elevators[bestElevator].step3(self.floors[randFloor])) # Thread of elevator
                    if not t[bestElevator].isAlive():
                        t[bestElevator].start()
                        print  t[bestElevator]

                    randTime = random.uniform(0.1, 1.0)
                    time.sleep(randTime)
                else:
                    self.floors[randFloor].pushPerson(person) # If there is no best elevator, person should wait until there is a best elevator
        for thread in t:
            t[thread].join()

        while (self.elevatorCheck() == False):
            for ele in self.elevators:
                if (ele.hasMoreStops()):
                    t[ele.getID()] = threading.Thread(target=self.elevators[ele.getID()].endStep())
                    t[ele.getID()].start()
        for thread in t:
            t[thread].join()

        for ele in self.elevators:
            self.totalTravelTime += ele.getTimeTraveled()
        answer = self.totalTravelTime / self.numberOfPeople
        return answer