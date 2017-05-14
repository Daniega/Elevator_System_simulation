import Person

from Person import Person

class Floor:

    """constructor"""
    def __init__(self, floorNum, numOfPeople, numOfFloors):
        self.floorNum = floorNum
        self.people = []
        self.peopleUp = []
        self.peopleDown = []

        for i in range(0, numOfPeople):
            self.people.append(Person(floorNum, numOfFloors))


    def addUp(self, floor):
        self.peopleUp.append(floor)

    def getFloor(self):
        return self.Floor

    def addDown(self, floor):
        self.peopleUp.append(floor)

    def getUps(self):
        return self.peopleUp

    def getDowns(self):
        return self.peopleDown

    def isNotEmpty(self):
        if len(self.people) != 0:
            return True
        else:
            return False

    def isEmpty(self):
        if len(self.people) == 0:
            return True
        else:
            return False

    def getPerson(self):
        if len(self.people) != 0 :
            return self.people.pop()
        else:
            return 'Empty'

    def pushPerson(self, person):
        self.people.append(person)

    def __repr__(self):
        return 'People in floor {} ({})'.format(self.floorNum, self.people)

