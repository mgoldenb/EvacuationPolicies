"""The "Compliant" policy:.

.. moduleauthor:: Meir Goldenberg <mgoldenbe@gmail.com>
"""
from policies.nearestExit import NearestExit
class Compliant:
    """The Compliant class for the policy that starts out as compliant
    
    Configuration:
    :ivar compliantColor: display color for the agent while it's compliant
    :ivar nearestColor: display for the agent while it's following the shortest path
    """
    def __init__(self, path, graph = None, exitDistances = None):
        """
        :param path: the path (list of nodes) computed by the centralized solver
        :param graph: the input graph. Needed to compute a new policy should the agent become non-compliant.
        :param exitDistances: distance from each node to the nearest exit. Needed to compute a new policy should the agent become non-compliant.
        """
        
        self.compliantColor = 'cyan'
        self.nearestColor = 'brown'
        self.policy = 'compliant'
        self.graph = graph
        self.exitDistances = exitDistances
        self.color = self.compliantColor
        self.path = path
        self.pos = 0
    
    def next(self):
        """
        :returns: The location for the next time step.
        """
        if self.pos >= len(self.path)-1: return self.path[-1]
        return self.path[self.pos + 1]
    
    def positiveFeedback(self):
        self.pos += 1

    def negativeFeedback(self, changeAllowedFlag):
        """
        :returns: Flag whether the policy has been changed and the simulation step needs to be redone.
        """
        if not changeAllowedFlag: return False
        if self.graph == None: return False
        if self.exitDistances == None: return False
        if self.policy != 'compliant': return False
        
        self.policy = 'nearest'
        self.color = self.nearestColor
        temp = NearestExit(self.graph, self.exitDistances, self.path[self.pos])
        self.path = self.path[:self.pos] + temp.path
        return True
        