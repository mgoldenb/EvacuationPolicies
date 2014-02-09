from common import *

class NearestExit:
    def __init__(self, graph, exitDistances, node):
        self.color = 'yellow'
        self.path = [node]
        while exitDistances[node]:
            neighbors = graph.neighbors(node)
            myDistances = {neighbor:exitDistances[neighbor] for neighbor in neighbors}
            node = min(myDistances, key = myDistances.get)
            self.path.append(node)
        self.pos = 0
    
    def next(self):
        if self.pos >= len(self.path)-1: return self.path[-1]
        return self.path[self.pos + 1]
    
    def positiveFeedback(self):
        self.pos += 1
        
    def negativeFeedback(self, changeAllowedFlag): return False