import random
import time
import threading

from Building import Building

numOfFloors = input('Enter amount of floors: ')
numOfElevators = input('Enter amount of elevators: ')


a = Building(15, numOfFloors, numOfElevators)
#b = Building(10, numOfFloors, numOfElevators)
a1 = a.simulateStrategy1()
#b2 = b.simulateStrategy2()

print a1
#print b.answer

