
from common import *

class Simulation:
    def __init__(self, instance, timeThreshold):
        self.instance = instance
        self.agents = agents = instance.agents
        self.policies = policies = instance.policies
        self.timeThreshold = timeThreshold
        self.paths = paths = [[agent] for agent in agents]
        self.colors = colors = [[policy.color] for policy in policies]
        self.directions = [[] for agent in agents]
    
        for time in range(1, timeThreshold + 1):
            self.resolutionDecisions = {}
            self.processConflicts(time)
            policyChanged = False
            for i in range(len(agents)):
                self.directions[i].append(self._wants[i])
                if not self._successFlags[i]:
                    if (policies[i].negativeFeedback(changeAllowedFlag = True)):
                        policyChanged = True
            if policyChanged: 
                self.processConflicts(time)
                
            for i in range(len(agents)):
                colors[i].append(policies[i].color)
                if self._successFlags[i]:
                    paths[i].append(self._wants[i])
                    policies[i].positiveFeedback()
                else:
                    paths[i].append(self._curs[i])
                    policies[i].negativeFeedback(changeAllowedFlag = False) 
    
    def processConflicts(self, time):
        self._successFlags = successFlags = [True] * len(self.agents)
        self._curs = [self.paths[i][time-1] for i in range(len(self.agents))]
        self._wants = [self.policies[i].next() for i in range(len(self.agents))]
        self.processTypedConflicts(time, "Collision")
        while True:
            nConflicts = self.processTypedConflicts(time, "IntoWaiting")
            if nConflicts == 0: break
            
    def processTypedConflicts(self, time, type):
        nConflicts = 0
        successFlags = self._successFlags
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
                        try: 
                            winner = self.resolutionDecisions[(i,j)] 
                        except:
                            winner = (i if random.randint(False, True) else j)
                        self.resolutionDecisions[(i,j)] = self.resolutionDecisions[(j,i)] = winner
                        if winner == j:
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
                    
                    