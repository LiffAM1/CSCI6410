import sys, os, traceback

# Node class for implementing singly-linked list
class Node:
    woman = None
    _next = None

    def __init__(self,_woman):
        self.woman = _woman

# Base class for Men and Women
class Person:
    number = 0

    def __init__(self,_number):
        self.number = _number

class Man(Person):
    preferences = None

    def __init__(self,_number,_preferences):
        Person.__init__(self,_number)

        self.preferences = _preferences

    # Method to allow a man to try to propose to a woman
    def propose(self):
        accepts,previousMatching = self.preferences.woman.acceptsProposal(self)

        # move on to the next in the preference list so that he doesn't propose to the same woman twice
        self.preferences = self.preferences._next

        return accepts,previousMatching

class Woman(Person):
    preferences = {}
    currentMatching = None

    def __init__(self,_number,_preferences):
        Person.__init__(self,_number)

        # use a hash set of the form {man:ranking,...} to hold preferences
        # can reference a man's ranking in constant time
        self.preferences = {m:i+1 for i,m in enumerate(_preferences)}

    # Method to determine wether the woman should accept a given proposal, based on the Gale Shapely algorithm
    def acceptsProposal(self,man):
        previousMatching = self.currentMatching

        # If she currently has no partner, accept 
        if self.currentMatching == None:
            self.currentMatching = man
            return (True,None)

        # otherwise, compare the rank of the new potential partner with her current partner
        currentMatchRanking = self.preferences[self.currentMatching.number]
        proposalRanking = self.preferences[man.number]
        if proposalRanking < currentMatchRanking:
            self.currentMatching = man
            return (True,previousMatching)

        return (False,None)


class GaleShapelyMatching:
    unmatchedMen = []
    women = {}

    matches = []

    def __init__(self,_men,_women):
        self.women = {w+1:Woman(w+1,preferences) for w,preferences in enumerate(_women)}
        self.unmatchedMen = [Man(m+1,self.buildLinkedList(preferences)) for m,preferences in enumerate(_men)]
        self.matches = self.match()

    # Method to build a singly linked list, which is used to store mens' preferences
    def buildLinkedList(self,preferences):
        head = None
        prev = None
        for p in preferences:
            node = Node(self.women[p])
            if (prev): prev._next = node
            if (not head): head = node
            prev = node


        return head

    # Method to generate the Gale Shapely stable matching set based on mens' and womens' preferences
    def match(self):
        # loop until the list of men is empty
        while len(self.unmatchedMen) > 0:
            man = self.unmatchedMen[0]
            accepts,previousMatching = man.propose()

            # if she accepts, remove the man from the list of unmatched men
            if accepts:
                self.unmatchedMen.pop(0)

                # if she had a previous matching, add him back to the list of unmatched men 
                if previousMatching:
                    self.unmatchedMen.append(previousMatching)

        # matches have the form [[man,woman],...]
        matches = [[w.currentMatching.number,w.number] for w in self.women.values()]
        return matches

class CheckMatchings:
    matchings = []

    partners = {}

    mensPreferences = []
    womensPreferences = []

    def __init__(self,_men,_women,_matchings):

        self.matchings = _matchings

        print("\nOutput:")
        print("===========================================")

        # First, check for perfect matches
        if not self.checkPerfection():
            return 

        # Dictionary comprehension so we can access preferences in constant time
        self.mensPreferences = {i+1:prefs for i,prefs in enumerate(_men)}
        self.womensPreferences = {i+1:{m:j+1 for j,m in enumerate(prefs)} for i,prefs in enumerate(_women)}

        # We want to be able to check a woman's current matching in constant time as well
        self.partners = {match[1]:match[0] for match in _matchings}

        # Check stability of matchings
        if self.checkStability():
            print("This set of matchings is perfect and stable!")

    # Method to check the perfection of a given set of matchings 
    def checkPerfection(self):
        matchedMen = [m[0] for m in self.matchings]
        matchedWomen = [m[1] for m in self.matchings]

        errors = []
        for m in set(matchedMen):
            if matchedMen.count(m) > 1:
                errors.append(f"Man {m} appears in {matchedMen.count(m)} couples.")
        for w in set(matchedWomen):
            if matchedWomen.count(w) > 1:
                errors.append(f"Woman {w} appears in {matchedWomen.count(w)} couples.")

        if errors:
            print("This set of matchings is not perfect because of the following reasons:")
            for e in errors:
                print(e)
            return False
        return True

    # Method to check the stability of a given set of matchings, based on mens' and womens' preferences
    def checkStability(self):
        errors = []

        for match in self.matchings:
            man = match[0]
            woman = match[1]

            # Check if it's a stable couple
            index = 0
            currentWoman = self.mensPreferences[man][index]
            while currentWoman != woman:
                preferences = self.womensPreferences[currentWoman]
                currentMatching = self.partners[currentWoman]
                if preferences[man] < preferences[currentMatching]:
                    errors.append(f"Man {man} and Woman {woman} are an unstable couple. Man {man} prefers Woman {currentWoman} and she prefers him over her current partner, Man {currentMatching}. Man {man} and Woman {currentWoman} may elope.")
                index += 1
                currentWoman = self.mensPreferences[man][index]
        if errors:
            print("This set of matchings is perfect but not stable because of the following reasons:")
            for e in errors:
                print(e)
            return False
        return True

class MainApplication:
    task = None
    mensPreferences = []
    womensPreferences = []
    matchings = []

    # Main method
    def __init__(self):
        # Get the command line arguments
        args = sys.argv

        if len(args) != 5:
            print("Error: incorrect number of arguments! Please try again!")
            return

        self.task = args[1]
        menFile = args[2]
        womenFile = args[3]
        matchingsFile = args[4]

        # Read in mens' and womens' preferences from indicated files
        self.mensPreferences = self.readFile(menFile)
        self.womensPreferences = self.readFile(womenFile)

        # Do either find or check task, depending on the input
        if (self.task == "find"):
            self.printInitialInput()
            self.writeFile(matchingsFile,GaleShapelyMatching(self.mensPreferences,self.womensPreferences).matches)
        elif (self.task == "check"):
            self.matchings = self.readFile(matchingsFile,False)
            self.printInitialInput()
            CheckMatchings(self.mensPreferences,self.womensPreferences,self.matchings)
        else:
            print("Error: invalid input! Please try again!")
            return

        print("\nAnalysis complete!")

    # User experience method for echoing back the input and pretty-printing the result
    def printInitialInput(self):
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        print("#############################################")
        print("# Welcome to the Stable Matchings Analysis! #")
        print("#############################################")
        print(f"\nTask: {self.task.capitalize()} stable matchings")
        if (self.task == "check"):
            print("\nMatchings to check:")
            print("===========================================")
            for m in self.matchings:
                print(f"Man {str(m[0])} and Woman {str(m[1])}")
        print("\nMen's Preferences:")
        print("===========================================")
        for i,m in enumerate(self.mensPreferences):
            print(f"Man {str(i+1)}:")
            print(", ".join([f"{str(ordinal(j+1))}: Woman {str(w)}" for j,w in enumerate(m)]))
        print("\nWomen's Preferences:")
        print("===========================================")
        for i,w in enumerate(self.womensPreferences):
            print(f"Woman {str(i+1)}:")
            print(", ".join([f"{str(ordinal(j+1))}: Man {str(m)}" for j,m in enumerate(w)]))

    # Method to read expected format from a file
    def readFile(self,fileName,skipFirst=True):
        file = open(fileName, 'r')
        result = []
  
        if skipFirst:
            file.readline()

        while True:
            line = file.readline()
            if not line:
                break
            result.append([int(l) for l in line.strip().split(" ")])
        file.close()
        return result

    # Method to write expected format to a file
    def writeFile(self,fileName,lines):
        lines = [" ".join([str(num) for num in l]) + "\n" for l in lines]
        file = open(fileName, 'w')
        file.writelines(lines)
        file.close()

MainApplication()
