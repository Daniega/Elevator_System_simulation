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

    """constructor"""

    def __init__(self, numberOfPeople, numOfFloors, numOfElevators):

        self.numberOfPeople = numberOfPeople
        self.numberOfFloors = numOfFloors
        self.floors = {}

        peopleInFloor = int(numberOfPeople / numOfFloors)

        for floorNum in range(1, numOfFloors + 1):
            self.floors[floorNum] = Floor(floorNum, peopleInFloor, numOfFloors)


        for i in range(0, numOfElevators):
            self.elevators.append(Elevator(i))

            # print self.elevators
            # print 'Floors: ', self.floors
    def floorCheck(self):
        for k,v in self.floors.items():
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
            print 'ID = ', elevator.getID(), 'Elevator floor = ', elevator.getFloor(), 'Elevator status = ', elevator.status()

            if len(elevator.listOfLoads) == 0:
                elevator.setDirection('idle')

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

    def simulateStrategy1(self):
        i = 0
        t = {}

        print 'FloorCheck: ', self.floorCheck(), 'ElevatorCheck: ', self.elevatorCheck()

        while (self.floorCheck() == False ):

            i = i + 1
            randFloor = random.randint(1, self.numberOfFloors)
            if not self.floors[randFloor].isEmpty():
                person = self.floors[randFloor].getPerson()

                """check person destination and add to floors list"""
                if person.direction == 'up':
                    self.floors[randFloor].addUp(person.destintaion())
                else:
                    self.floors[randFloor].addDown(person.destintaion())

                print 'Source = ', person.getFloor(), 'Destination = ', person.destintaion(), 'Direction = ', person.direction()
                bestElevator = self.optimalElevatorID(person.floor, person.direction())
                if bestElevator != -1:
                    print 'bestElevator = ', bestElevator
                    self.elevators[bestElevator].addToLoads(person.getFloor())
                    t[bestElevator] = threading.Thread(target=self.elevators[bestElevator].step(self.floors[randFloor]))
                    if not t[bestElevator].isAlive():
                        t[bestElevator].start()

                    randTime = random.uniform(0.1, 1.0)
                    time.sleep(randTime)
                else:
                    self.floors[randFloor].pushPerson(person)
        print 'Number of iterations = ', i
        print t
        for thread in t:
            t[thread].join()

        while (self.elevatorCheck() == False):
            for ele in self.elevators:
                if(ele.hasMoreStops()):
                    t[ele.getID()] = threading.Thread(target=self.elevators[ele.getID()].endStep())
                    t[ele.getID()].start()
        for thread in t:
            t[thread].join()

        for ele in self.elevators:
            print ele
        print t
        for ele in self.elevators:
            self.totalTravelTime += ele.getTimeTraveled()

        return self.totalTravelTime / self.numberOfPeople


        # while(not all(self.floors[i].isEmpty() for i in range(1, numOfFloors))):
        # randInvite = random.randint(1, numOfFloors)
        #
        # if (self.elevators[randInvite])
        # for i in range(1, numOfElevators):
