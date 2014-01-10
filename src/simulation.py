
from common import *

class Simulation:
    def __init__(self, instance, timeThreshold):
        self.instance = instance
        self.agents = agents = instance.agents
        self.policies = policies = instance.policies
        self.timeThreshold = timeThreshold
        self.paths = paths = [[agent] for agent in agents]
        self.directions = [policy.direction() for policy in policies]
    
        for time in range(1, timeThreshold + 1):
            self.successFlags = successFlags = [True] * len(agents)
            self.processConflicts(time, "Collision")
            self.processConflicts(time, "IntoWaiting")
            for i in range(len(agents)):
                paths[i][time] = (policies[i].next() if successFlags[i] 
                                  else paths[i][time-1])
                 
    def processConflicts(self, time, type):
        successFlags = self.successFlags; 
        agents = self.agents; paths = self.paths; policies = self.policies
        for i in range(len(agents)):
            if not successFlags[i]: continue
            i_cur = paths[i][time-1]
            i_wants = policies[i].next()
            for j in range(0,i):
                j_cur = paths[j][time-1]
                j_wants = policies[j].next()
                if i_wants == j_wants:
                    if type == "Collision":
                        if random.randint(False, True):
                            successFlags[i] = False
                            break
                        else:
                            successFlags[j] = False
                            continue
                    if type == "IntoWaiting":
                        if j_cur == j_wants or not successFlags[j]:
                            successFlags[i] = False
                            break
                        if i_cur == i_wants or not successFlags[i]:
                            successFlags[j] = False
                            continue
                    
                    