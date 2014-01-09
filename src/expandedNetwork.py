from common import *

from pygraph.algorithms.searching import breadth_first_search
from pygraph.algorithms.minmax import maximum_flow

sourceID = -1
sinkID = -2

class ExpandedNetwork:
    def _getNetworkID(self, layoutNode, time, stage):
        return (2*time + stage) * (self.instance.maxNodeID + 1) + layoutNode

    def __init__(self, instance, maxTime):
        self.instance = instance
        self.capacities = {}
        self.nodeToLayout = {}
        self.nodeToStage = {}
        print("Building the network...")
        self.graph = graph = digraph()
    
        # add nodes
        graph.add_node(sourceID)
        graph.add_node(sinkID)
        for time in range(0, maxTime + 1):
            for layoutNode in instance.graph.nodes():
                for stage in range(2):
                    nodeID = self._getNetworkID(layoutNode, time, stage)
                    graph.add_node(nodeID)
                    self.nodeToLayout[nodeID] = layoutNode
                    self.nodeToStage[nodeID] = stage

        # arcs from source
        for i in instance.agents:
            toNode = self._getNetworkID(i, time = 0, stage = 1)
            self.graph.add_edge((sourceID, toNode))
            self.capacities[(sourceID, toNode)] = 1
        
        # arcs between time layers (from (time) to (time + 1)) and from exits to sink
        for time in range(0, maxTime + 1):
            for layoutFrom in instance.graph.nodes():
                fromNode = self._getNetworkID(layoutFrom, time = time, stage = 1)
                if layoutFrom in instance.exits:
                   self.graph.add_edge((fromNode, sinkID))
                   self.capacities[(fromNode, sinkID)] = INFINITY
                   continue
                if time > maxTime - 1: continue  
                for layoutTo in instance.graph.neighbors(layoutFrom) + [layoutFrom]:
                    toNode = self._getNetworkID(layoutTo, time = time + 1, stage = 0)
                    self.graph.add_edge((fromNode, toNode))
                    self.capacities[(fromNode, toNode)] = 1 
        
        # arcs between stages of the same time layer (no need for layer 0)
        for time in range(1, maxTime + 1):
            for layoutNode in instance.graph.nodes():
                fromNode = self._getNetworkID(layoutNode, time = time, stage = 0)
                toNode = self._getNetworkID(layoutNode, time = time, stage = 1)
                capacity = INFINITY if layoutNode in instance.exits else 1
                self.graph.add_edge((fromNode, toNode))
                self.capacities[(fromNode, toNode)] = capacity
            
        print("Before removing unneeded nodes: {0} nodes".format(len(self.graph.nodes())))    
        # Removing unused nodes, i.e. nodes unreachable from either source or sink
        tree1,_ = breadth_first_search(self.graph, sourceID)
        print("Spanning tree from source: {0} nodes".format(len(tree1)))    
    
        tree2,_ = breadth_first_search(self.graph.reverse(), sinkID)
        print("Spanning tree from sink: {0} nodes".format(len(tree2)))
        
        for i in self.graph.nodes():
            if i in tree1 and i in tree2:
                continue
            self.graph.del_node(i)
        print("After removing unneeded nodes: {0} nodes".format(len(self.graph.nodes())))    

    @timing
    def solveMaxFlow(self):
        instance = self.instance
        flow, _ = maximum_flow(self.graph, sourceID, sinkID, self.capacities)
        # form the reduced network in which only arcs with flow are present
        reducedNetwork = digraph()
        reducedNetwork.add_graph(self.graph) # does not add node attributes
        for arc in self.graph.edges():
            if flow[arc] == 0:
                reducedNetwork.del_edge(arc)
        for node in self.graph.nodes():
            if reducedNetwork.neighbors(node) == []:
                reducedNetwork.del_node(node)
        
        # form paths for agents
        solution = []
        for i in range(instance.nAgents):
            nodeID = self._getNetworkID(instance.agents[i], time = 0, stage = 1)
            layoutNode = self.nodeToLayout[nodeID]
            stage = 1   
            solution.append([])
            while (True):
                if (stage == 1):
                    solution[i].append(layoutNode)
                    if layoutNode in instance.exits:
                        break
                try:
                    neighbors = reducedNetwork.neighbors(nodeID)
                except:
                    break # nodeID is not in the network: the agent is too far from exit
                if (neighbors == []):
                    break
                if (len(neighbors) > 1):
                    print("More than one possibility in the solution!")
                    exit()
                nodeID = neighbors[0]
                layoutNode = self.nodeToLayout[nodeID]
                stage = self.nodeToStage[nodeID]
        return solution