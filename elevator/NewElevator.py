import random
import time
import threading

from Building import Building

numOfFloors = input('Enter amount of floors: ')
numOfElevators = input('Enter amount of elevators: ')


b = Building(50, numOfFloors, numOfElevators)
tot = b.simulateStrategy1()
print tot

