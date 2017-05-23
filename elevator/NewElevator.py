import random
import time
import threading

from Building import Building


print "Enter amount of floors, and amount of elevators:"
try:
    numOfFloors = input('Enter amount of floors: ')
    numOfElevators = input('Enter amount of elevators: ')
except(ValueError, TypeError, NameError):
    print 'Only integer numbers allowed'


a = Building(15, numOfFloors, numOfElevators)
b = Building(15, numOfFloors, numOfElevators)
c = Building(15, numOfFloors, numOfElevators)
a1 = a.simulateStrategy1()
b2 = b.simulateStrategy2()
c3 = c.simulateStrategy3()

print 'Average waiting time Base model = {} seconds'.format(a1*100)
print 'Average waiting time Strategy2 = {} seconds'.format(b2*100)
print 'Average waiting time Strategy4 = {} seconds'.format(c3*100)


#print b.answer

