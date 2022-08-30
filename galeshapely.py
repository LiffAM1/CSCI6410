import sys, os, traceback

class Man:
    number = 0

    preferences = []
    currentIndex = 0

    def __init__(self,_number,_preferences):
        self.number = _number
        self.preferences = _preferences

    def propose(self,woman):
        # always increment the current index so he doesn't propose to the same woman twice
        self.currentIndex += 1
        return woman.acceptsProposal(self)

class Woman:
    number = 0

    preferences = {}
    currentMatching = None

    def __init__(self,_number,_preferences):
        self.number = _number
        # use a hash set of the form {man:ranking,...} to hold preferences
        # can reference a man's ranking in constant time
        self.preferences = {m:i for i,m in enumerate(_preferences)}

    def acceptsProposal(self,man):
        previousMatching = self.currentMatching
        # If she currently has no partner, then accept
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
    men = []
    women = []

    matches = None

    def __init__(self,_men,_women):
        # initial men and woman lists
        for i,preferences in enumerate(_men):
            self.men.append(Man(i+1,preferences))

        for i,preferences in enumerate(_women):
            self.women.append(Woman(i+1,preferences))

    def match(self):
        # loop until the list of men is empty
        while len(self.men) > 0:
            man = self.men[0]
            accepts,previousMatching = man.propose(self.women[man.preferences[man.currentIndex]-1])
            if accepts:
                self.men.pop(0)

                if previousMatching:
                    self.men.append(previousMatching)

        # matches have the form [[woman,man],...]
        self.matches = [[w.number,w.currentMatching.number] for w in self.women]
        print(self.matches)


# women = [Amy(1),Bertha(2),Clare(3),Diane(4),Erika(5)]
# men = [Victor(1),Wyatt(2),Xavier(3),Yancey(4),Zeus(5)]

galeShapely = GaleShapelyMatching([[2,1,4,5,3],[4,2,1,3,5],[2,5,3,4,1],[1,4,3,2,5],[2,4,1,5,3]],[[5,1,2,4,3],[3,2,4,1,5],[2,3,4,5,1],[1,5,4,3,2],[4,2,5,3,1]])
galeShapely.match()
