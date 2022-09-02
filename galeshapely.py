import sys, os, traceback

# Node class for implementing singly-linked list
class Node:
    woman = None
    _next = None

    def __init__(self,_woman):
        self.woman = _woman

class Person:
    number = 0

    def __init__(self,_number):
        self.number = _number

class Man(Person):
    preferences = None

    def __init__(self,_number,_preferences):
        Person.__init__(self,_number)

        self.preferences = _preferences

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

    matches = None

    def __init__(self,_men,_women):
        self.women = {w+1:Woman(w+1,preferences) for w,preferences in enumerate(_women)}
        self.unmatchedMen = [Man(m+1,self.buildLinkedList(preferences)) for m,preferences in enumerate(_men)]
        self.match()

    def buildLinkedList(self,preferences):
        head = None
        prev = None
        for p in preferences:
            node = Node(self.women[p])

            if (prev): prev._next = node

            if (not head): head = node
            prev = node


        return head

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
        self.matches = [[w.currentMatching.number,w.number] for w in self.women.values()]
        print(self.matches)

class CheckMatchings:
    matchings = []

    partners = {}

    mensPreferences = []
    womensPreferences = []

    errors = []
    def __init__(self,_men,_women,_matchings):
        # First, check for perfect matches
        matchedMen = [m[0] for m in _matchings]
        matchedWomen = [m[1] for m in _matchings]
        for m in set(matchedMen):
            if matchedMen.count(m) > 1:
                self.errors.append(f"Man {m} appears in {matchedMen.count(m)} couples.")
        for w in set(matchedWomen):
            if matchedWomen.count(w) > 1:
                self.errors.append(f"Woman {w} appears in {matchedWomen.count(w)} couples.")

        if self.errors:
            print("This set of matchings is not perfect because of the following reasons:")
            for e in self.errors:
                print(e)
            return

        # If the couples are all perfect matches, we can check each for stability

        # Dictionary comprehension so we can access preferences in constant time
        self.mensPreferences = {i+1:prefs for i,prefs in enumerate(_men)}
        self.womensPreferences = {i+1:{m:j+1 for j,m in enumerate(prefs)} for i,prefs in enumerate(_women)}

        self.matchings = _matchings
        self.partners = {match[1]:match[0] for match in _matchings}

        self.checkStability()

        if self.errors:
            print("This set of matchings is perfect but not stable because of the following reasons:")
            for e in self.errors:
                print(e)
        else:
            print("This set of matchings is perfect and stable!")


    def checkStability(self):
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
                    self.errors.append(f"Man {man} and Woman {woman} are an unstable couple. Man {man} prefers Woman {currentWoman} and she prefers him over her current partner, Man {currentMatching}. Man {man} and Woman {currentWoman} may elope.")
                index += 1
                currentWoman = self.mensPreferences[man][index]




# women = [Amy(1),Bertha(2),Clare(3),Diane(4),Erika(5)]
# men = [Victor(1),Wyatt(2),Xavier(3),Yancey(4),Zeus(5)]

GaleShapelyMatching([[2,1,4,5,3],[4,2,1,3,5],[2,5,3,4,1],[1,4,3,2,5],[2,4,1,5,3]],[[5,1,2,4,3],[3,2,4,1,5],[2,3,4,5,1],[1,5,4,3,2],[4,2,5,3,1]])
CheckMatchings([[2,1,4,5,3],[4,2,1,3,5],[2,5,3,4,1],[1,4,3,2,5],[2,4,1,5,3]],[[5,1,2,4,3],[3,2,4,1,5],[2,3,4,5,1],[1,5,4,3,2],[4,2,5,3,1]],[[1, 1], [1, 1], [2, 3], [5, 3], [4, 5]])
