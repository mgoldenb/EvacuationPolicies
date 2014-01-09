from common import *
class Instance:
    """ 
    Provides methods for working with the building layout
    Members:
        graph -- the underlying graph
        nNodes -- number of nodes in the graph
        maxNodeID -- maximal node ID
        nodeToRC -- map of grid coordinates (row, column)
        rcToNode -- reverse map
        maxRow, maxColumn, nRows, nColumns
        exits -- list of exits
        agents -- initial locations of all agents
        nAgents -- number of agents (including hats)
        hats -- initial locations of agents that have to be saved
    """
    def _makeCompleteGrid(self):
        nodeID = 0
        for row in range(self.nRows):
            for column in range(self.nColumns):
                self.graph.add_node(nodeID)
                self.nodeToRC[nodeID] = (row,column)
                self.rcToNode[(row, column)] = nodeID
                nodeID += 1
        for row in range(self.nRows):
            for column in range(self.nColumns):
                myNode = self.rcToNode[(row, column)]
                if column > 0: self.graph.add_edge((myNode, self.rcToNode[(row, column - 1)]))
                if column < self.nColumns - 1: self.graph.add_edge((myNode, self.rcToNode[(row, column + 1)]))
                if row > 0: self.graph.add_edge((myNode, self.rcToNode[(row - 1, column )]))
                if row < self.nRows - 1: self.graph.add_edge((myNode, self.rcToNode[(row + 1, column )])) 
    
    def __init__(self, fileName):
        self.graph = digraph()
        self.nodeToCoords = {}
        file = open(fileName)
        self.nRows, self.nColumns = [int(n) for n in file.readline().split()]
        self.maxRow, self.maxColumn = self.nRows - 1, self.nColumns - 1
        self.nodeToRC = {}
        self.rcToNode = {}
        
        self._makeCompleteGrid()
        
        self.exits = []
        self.agents = []
        self.hats = []
        for row, line in enumerate(file):
            for column, char in enumerate(line.strip()):
                myNode = self.rcToNode[(row, column)]
                if (char == '@'): 
                    self.graph.del_node(myNode)
                    self.rcToNode.pop((row, column))
                if (char == 'e'): self.exits.append(myNode)
                if (char == 'a' or char == 'h'): self.agents.append(myNode)
                if (char == 'h'): self.hats.append(myNode)
        self.nNodes = len(self.graph.nodes())
        self.maxNodeID = max(self.graph.nodes())
        self.nAgents = len(self.agents) 
        #random.shuffle(self.agents)