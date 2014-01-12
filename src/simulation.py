
from common import *

class Simulation:
    def __init__(self, instance, timeThreshold):
        self.instance = instance
        self.agents = agents = instance.agents
        self.policies = policies = instance.policies
        self.timeThreshold = timeThreshold
        self.paths = paths = [[agent] for agent in agents]
        self.directions = [[] for agent in agents]
    
        for time in range(1, timeThreshold + 1):
            self._successFlags = successFlags = [True] * len(agents)
            self._curs = [paths[i][time-1] for i in range(len(agents))]
            self._wants = [policies[i].next() for i in range(len(agents))]
            self.processConflicts(time, "Collision")
            while True:
                nConflicts = self.processConflicts(time, "IntoWaiting")
                if nConflicts == 0: break
            for i in range(len(agents)):
                self.directions[i].append(self._wants[i])
                if successFlags[i]:
                    paths[i].append(self._wants[i])
                    policies[i].feedback(True)
                else:
                    paths[i].append(self._curs[i])
                    policies[i].feedback(False) 
                 
    def processConflicts(self, time, type):
        nConflicts = 0
        successFlags = self._successFlags; 
        agents = self.agents; 
        for i in range(len(agents)):
            i_cur = self._curs[i]
            i_wants = (self._wants[i] if successFlags[i] else i_cur)
            if i_wants in self.instance.exits: continue
            for j in range(0,i):
                j_cur = self._curs[j]
                j_wants = (self._wants[j] if successFlags[j] else j_cur)
                if j_wants in self.instance.exits: continue
                if i_wants == j_wants:
                    nConflicts += 1
                    if type == "Collision":
                        if i_cur == i_wants or j_cur == j_wants: continue
                        if random.randint(False, True):
                            successFlags[i] = False
                            break
                        else:
                            successFlags[j] = False
                            continue
                    if type == "IntoWaiting":
                        if j_cur == j_wants:
                            successFlags[i] = False
                            break
                        if i_cur == i_wants:
                            successFlags[j] = False
                            break
        return nConflicts
                    
                    