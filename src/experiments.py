from common import *
import gui
from instance import Instance
import expandedNetwork
import solveNetworkLIP
from solution import Solution
from simulation import Simulation
from policies import compliant
from policies import nearestExit

class Experiment:
    def makeMD5Data(self, instance, timeThreshold):
        myNodes = instance.graph.nodes(); myNodes.sort()
        myEdges = instance.graph.edges(); myEdges.sort()
        myExits = instance.exits; myExits.sort()
        myAgents = instance.agents; myAgents.sort
        return [myNodes, myEdges, myExits, myAgents, timeThreshold]
    
    def solveMaxFlow(self, instance, timeThreshold):
        storedSolutionFileName = '../storedSolutions/' + dataToMD5(self.makeMD5Data(instance, timeThreshold))
        try:
            storedSolution = open(storedSolutionFileName)
            import ast
            print("Found a ready solution!")
            # the following works for now
            # need to be careful when paths of agents aren't ordered 
            # according to the agents' current location
            maxFlowPaths = [ast.literal_eval(myStr) for myStr in storedSolution]
        except: 
            print("Solving by MaxFlow...")
            network = expandedNetwork.ExpandedNetwork(instance, timeThreshold)
            maxFlowPaths = network.solveMaxFlow()
            storedSolutionFile = open(storedSolutionFileName, mode='w')
            for path in maxFlowPaths:
                print(path, file = storedSolutionFile)
        solution = Solution(maxFlowPaths, instance.exits) 
        solution.checkSolution(fixFlag = True)
        #printPlan(instance, simulation)
        solution.checkSolution()
        return solution
        
    def __init__(self, inputFileName, timeThreshold = INFINITY, substitutePolicies = None):
        self.instance = instance = Instance(inputFileName)
        if substitutePolicies != None: instance.policies = [substitutePolicies] * instance.nAgents
        compliantPolicies = ['c', 's']
        for policy in instance.policies: 
            if policy in compliantPolicies:
                solution = self.solveMaxFlow(instance, timeThreshold)
                break
        
        for i, policy in enumerate(instance.policies[:]):
            if policy == 'c': # compliant no matter what
                instance.policies[i] = compliant.Compliant(solution.paths[i])
                continue
            if policy == 's': # compliant, but switches to nearest exit if cannot be compliant
                instance.policies[i] = compliant.Compliant(solution.paths[i], instance.graph, instance.exitDistances)
                continue
            if policy == 'n': 
                instance.policies[i] = \
                nearestExit.NearestExit(instance.graph, instance.exitDistances, instance.agents[i])
                continue
            print("An unknown policy " + str(policy))
            
        self.simulation = Simulation(instance, timeThreshold)

def main():
    if sys.argv[1:]:
        inputSource = sys.argv[1]
    else: # if running as script
        #inputSource = '../instances/simplest.txt'
        #inputSource = '../instances/two_lines.txt'
        
        #inputSource = '../instances/balancing.txt'
        #timeThreshold = 20
        
        #inputSource = '../instances/balancing_simple.txt'
        #timeThreshold = 5
        
        #inputSource = '../instances/conflict_pays.txt'
        #timeThreshold = 15
        
        #inputSource = '../instances/counter_example/changing_policy.txt'
        #timeThreshold = 19
        
        inputSource = '../instances/ready/'
        
    
    batchMode = (True if inputSource[-1]=='/' else False)
    inputFileNames = (glob.glob(inputSource + "*.txt") if batchMode else [inputSource])
    inputFileNames.sort()
    nPastExperiments = 0
    curExperiment = -1
    if batchMode:
        try:
            nPastExperiments = sum(1 for _ in open(inputSource + "results.out"))
        except:
            pass
    if batchMode:
        output = open(inputSource + "results.out", mode='a')
    #print([os.path.basename(inputFileName) for inputFileName in inputFileNames])
    #exit(1)
    for inputFileName in inputFileNames:
        shortFileName = os.path.basename(inputFileName)
        random.seed(1001)
        nearestExperiment = Experiment(inputFileName, substitutePolicies = 'n')
        baseTime = nearestExperiment.simulation.timeThreshold
        timeThresholds = [int(percentage * baseTime/100) for percentage in [100, 90, 80, 70]]
        for timeThreshold in timeThresholds:
            print("\nMap: " + shortFileName + "   Threshold: " + str(timeThreshold))
            curExperiment += 1
            if curExperiment < nPastExperiments:
                continue
            myExperiment = Experiment(inputFileName, timeThreshold = timeThreshold)
            if batchMode:
                outputString = ""
                outputString += " " + shortFileName[:shortFileName.index('-')] # map name
                outputString += " " + str(myExperiment.instance.nAgents)
                # append the number of non-compliant agents
                ncIndex = shortFileName.index('NC')+3
                outputString += " " + shortFileName[ncIndex:shortFileName.index('-',ncIndex)]
                instanceIndex = shortFileName.index('-I')+2
                outputString += " " + shortFileName[instanceIndex:shortFileName.index('.',instanceIndex)]
                outputString += " " + str(timeThreshold)
                outputString += " " + str(myExperiment.simulation.nSaved)
                print(outputString, file=output)
            else:
                print("OUTPUT: " + outputString)
                continue
                print("Showing the simulation graphically...")    
                # Create the graphical objects...
                h = gui.TkEvac(myExperiment.instance, myExperiment.simulation, nSteps = 20, stepTime = 500)
                h.run()
    print("Script Done!")

# Call main when run as script
if __name__ == '__main__':
    main() 