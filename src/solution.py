from common import *

#debugFixesFlag = True
debugFixesFlag = False

class Solution:
    def __init__(self, paths, exits=[]):
        self.paths = paths
        self.exits = exits
        self.longestPathLength = max([len(path) for path in self.paths])
        self.expandedPaths = [path + path[-1:]*(self.longestPathLength-len(path)) for path in paths]
    
    def isAgentSaved(self, i):
        return (self.expandedPaths[i][-1] in self.exits)
    
    def doAgentsExchange(self, i, j, time):
        """Do agents i and j exchange places from time-1 to time"""
        expandedPaths = self.expandedPaths
        if (expandedPaths[i][time] == expandedPaths[i][time - 1]): return False
        if (expandedPaths[i][time] != expandedPaths[j][time - 1]): return False
        if (expandedPaths[j][time] != expandedPaths[i][time - 1]): return False
        return True
    
    def fixExchange(self, i, j, time):
        expandedPaths = self.expandedPaths
        expandedPaths[i][time:], expandedPaths[j][time:] = expandedPaths[j][time:], expandedPaths[i][time:]
        
    def doAgentsOverlap(self, i, j, time):
        """Do agents i and j occupy the same place at time"""
        expandedPaths = self.expandedPaths
        node1 = expandedPaths[i][time]
        node2 = expandedPaths[j][time]
        if (node1 in self.exits): return False # no need to check node2
        if (node1 != node2): return False
        return True
    
    # Agent i is non-saved
    # Any non-saved agents' conflicts that will result from fixes, will be handled by recursion
    def fixOverlaps(self, i, tb):
        expandedPaths = self.expandedPaths
        node = expandedPaths[i][tb]
        try:
            # find an agent j != i who wants to pass 'node' at 'myTime'
            j = [path[tb] for path in expandedPaths[0:i]+expandedPaths[i+1:]].index(node)
            if j >= i: j += 1
        except:
            return
        if not self.isAgentSaved(j):
            print("Mixed invariant broken")
            exit()
        if expandedPaths[j][tb] == expandedPaths[j][tb]-1:
            print("Agent b was there before tb!")
            exit()
        delta_tb = getRepLength(expandedPaths[j][tb:]) - 1 # for how long j occupies 'node'
        expandedPaths[i][tb+delta_tb+1:] = expandedPaths[j][tb+delta_tb+1:]
        expandedPaths[j][tb:] = [expandedPaths[j][tb-1]] * len(expandedPaths[j][tb:])
        self.nFixes += 1
        if debugFixesFlag: print("Fix: " + str(expandedPaths))
        self.fixOverlaps(j, tb)
    
    def checkSolutionForOverlaps(self, fixFlag = False):
        okFlag = True
        self.nFixes = 0
        for time in range(1, self.longestPathLength):
            if debugFixesFlag: print("Time " + str(time))
            for i in range(len(self.expandedPaths)):
                if fixFlag:
                    if not self.isAgentSaved(i):
                        self.fixOverlaps(i, time)
                        #print('time:' + str(time) + '    ' + str(self.expandedPaths))
                    continue
                for j in range(i):
                    if self.doAgentsOverlap(i, j, time):
                        print("Agents {0} and {1} overlap at time {2}".format(i, j, time))
                        #okFlag = False
        if not okFlag: exit()
        
    def checkSolutionForExchanges(self, fixFlag = False):
        okFlag = True
        for time in range(self.longestPathLength):
            for i in range(len(self.paths)):
                for j in range(i):
                    if self.doAgentsExchange(i, j, time):
                        if not fixFlag:
                            print("Agents {0} and {1} exchange at time {2}".format(i, j, time))
                            #okFlag = False
                        else: self.fixExchange(i, j, time)
        if not okFlag: exit()
    
    def checkSolution(self, fixFlag = False):
        print("Checking the solution for exchanges and overlaps...")
        self.checkSolutionForExchanges(fixFlag)
        #print(solution.expandedPaths)
        self.checkSolutionForOverlaps(fixFlag)
        if fixFlag: print("Made " + str(self.nFixes) + " fixes")
        self.paths = self.expandedPaths

# solution = Solution([[0, 0, 2, 5, 7, 12], [9, 9, 9, 2, 6, 11], [1, 2, 3, 3, 4, 10], [3, 3, 3, 3, 3, 3]])
# solution = Solution([[100, 100, 100, 100, 100, 100, 100, 100, 100], 
#                        [101, 101, 100, 100, 100, 100, 111, 211, 311],
#                        [102, 102, 102, 101, 101, 112, 212, 312, 412],
#                        [103, 103, 101, 113, 213, 313, 413, 513, 613]], 
#                     [311, 412, 613])
# solution.checkSolution(fixFlag = True)
# solution.checkSolution()