from tkinter import *
import tkinter.font as tkfont

def create_circle(canvas, x, y, r, fill):
    return canvas.create_oval(x-r, y-r, x+r, y+r, fill)

def computeFont(text, width, height):
    size = 6
    while True:
        font = tkfont.Font(family="Times", size=size)
        if font.metrics("linespace") > height:
            break
        if font.measure(text) > width:
            break
        size += 1
    return tkfont.Font(family="Times", size=size - 1)
        
# The graphical interface
class TkEvac:
    def __init__(self, instance, simulation, nSteps, stepTime):
        self.instance = instance
        self.simulation = simulation
        self.paths = simulation.paths
        self.directions = simulation.directions
        self.nSteps = nSteps
        self.stepTime = stepTime
        self.tk = tk = Tk()
        
        #self._geom='200x200+0+0'
        width = int(0.9 * tk.winfo_screenwidth())
        height = int(0.9 * tk.winfo_screenheight())
        tk.geometry("{0}x{1}+{2}+{3}"
                    .format(width, height,  
                            int((tk.winfo_screenwidth()-width)/2), int((tk.winfo_screenheight()-height)/2)))
        
        self.canvas = canvas = Canvas(tk, width = width, height = height)
        canvas.pack()
        
        self.layoutHeight = layoutHeight = int(height * 0.8)
        self.titleWidth = titleWidth = width
        self.titleHeight = titleHeight = int(height * 0.1)
        self.buttonsWidth = width
        self.buttonsHeight = titleHeight = int(height * 0.1) 
        self.cellSize = min(width/instance.nColumns, layoutHeight/instance.nRows)
        self.graphieSize = 0.6 * self.cellSize
        
        buttons = []
        buttons.append(("stepForward", Button(tk, text="Step >", command=self.stepForward)))
        buttons.append(("stepBack", Button(tk, text="Step <", command=self.stepBack)))
        buttons.append(("playForward", Button(tk, text="Play >", command=self.playForward)))
        buttons.append(("Reset", Button(tk, text="Reset", command=self.reset)))
        buttonWidth = self.buttonsWidth/len(buttons)
        for i, (buttonName, button) in enumerate(buttons):
            button.place(x=i * buttonWidth, y = titleHeight)
        
        self.titleFont = computeFont(self.computeTitleString(simulation.timeThreshold, len(simulation.paths)),
                                     width, titleHeight)
        self.agentFont = computeFont(str(len(simulation.paths)-1), self.graphieSize, self.graphieSize)
        self.exitFont = computeFont(str(len(instance.exits)-1), self.cellSize, self.cellSize)
        
        self.lastTime = 0
        self.time = 0
        self.drawTimeStep()
        #self.tk.update()
    
    def drawDirection(self, cur, nxt):
        if cur == nxt: return
        cur_row, cur_column = self.instance.nodeToRC[cur]
        next_row, next_column = self.instance.nodeToRC[nxt]
        curX, curY = self.computeCenterXY(cur_row, cur_column)
        if (next_row == cur_row + 1):
            self.canvas.create_polygon(curX - self.graphieSize/2, curY + self.graphieSize/2,
                                       curX + self.graphieSize/2, curY + self.graphieSize/2,
                                       curX, curY + self.cellSize/2)
        if (next_row == cur_row - 1):
            self.canvas.create_polygon(curX - self.graphieSize/2, curY - self.graphieSize/2,
                                       curX + self.graphieSize/2, curY - self.graphieSize/2,
                                       curX, curY - self.cellSize/2)
        if (next_column == cur_column + 1):
            self.canvas.create_polygon(curX + self.graphieSize/2, curY - self.graphieSize/2,
                                       curX + self.graphieSize/2, curY + self.graphieSize/2,
                                       curX + self.cellSize/2, curY)
        if (next_column == cur_column - 1):
            self.canvas.create_polygon(curX - self.graphieSize/2, curY - self.graphieSize/2,
                                       curX - self.graphieSize/2, curY + self.graphieSize/2,
                                       curX - self.cellSize/2, curY)
        
    def reset(self):
        self.lastTime = self.time
        self.time = 0
        self.drawTimeStep()
        #self.tk.update()
        
    def stepForward(self):
        self.lastTime = self.time
        self.time += 1
        self.drawTimeStep()
        #self.tk.update()
        
    def stepBack(self):
        self.lastTime = self.time
        self.time -= 1
        self.time = max(0, self.time)
        self.drawTimeStep()
        #self.tk.update()
    
    def playForward(self):
        while self.time < self.simulation.timeThreshold:
            self.lastTime = self.time
            self.time += 1
            self.drawTimeStep()
            #self.tk.update()
            self.tk.after(int(self.stepTime/2))
    
    def computeTitleString(self, time, saved):
        res = "Time: " + str(time) + "(of " + str(self.simulation.timeThreshold) + ")" + \
        "   Saved: " + str(saved) +"(of " + str(len(self.simulation.paths)) + ")"
        return res
    
    def computeXY(self, row, column):
        cellSize = self.cellSize;
        return column * cellSize, self.titleHeight + self.buttonsHeight + row * cellSize
    
    def computeCenterXY(self, row, column):
        cornerX, cornerY = self.computeXY(row, column)
        return cornerX + self.cellSize/2, cornerY + self.cellSize/2
        
    def drawGrid(self, time):
        instance = self.instance; cellSize = self.cellSize; canvas = self.canvas
        saved = 0
        for row in range(instance.nRows):
            for column in range(instance.nColumns):
                cornerX, cornerY = self.computeXY(row, column)
                centerX, centerY = self.computeCenterXY(row, column)
                text = ""
                try:
                    node = instance.rcToNode[(row, column)]
                    color = 'gray'
                except:
                    color = 'black'
                canvas.create_rectangle(cornerX, cornerY, cornerX + cellSize, cornerY + cellSize, {'fill': color})
        
    def drawExits(self, time):
        instance = self.instance; cellSize = self.cellSize; canvas = self.canvas
        saved = 0
        for exit in instance.exits:
            row, column = instance.nodeToRC[exit]
            cornerX, cornerY = self.computeXY(row, column)
            centerX, centerY = self.computeCenterXY(row, column)
            mySaved = self.nAgentsAtExit(exit, time)
            text = str(mySaved)
            saved += mySaved
            color = 'green'
            canvas.create_rectangle(cornerX, cornerY, cornerX + cellSize, cornerY + cellSize, {'fill': color})
            canvas.create_text(centerX, centerY, text = text, fill="black", font=self.exitFont)
        canvas.create_rectangle(0, 0, self.titleWidth, self.titleHeight, {'fill': "white"})
        canvas.create_text(self.titleWidth/2, self.titleHeight/2, text = self.computeTitleString(time, saved), 
                           fill="black", font=self.titleFont)
        
    def nAgentsAtExit(self, e, time):
        paths = self.paths
        res = 0
        for i in range(len(paths)):
            if self.simulation.paths[i][time] == e:
                res += 1
        return res
    
    def drawTimeStep(self):
        instance = self.instance; paths = self.paths; canvas = self.canvas
        nSteps = self.nSteps
        canvas.delete("all")
        for step in range(1,nSteps+1):
            self.drawGrid(self.time)
            for i in range(len(paths)):
                curNode = paths[i][self.time]
                lastNode = paths[i][self.lastTime]
                row, column = instance.nodeToRC[curNode]
                lrow, lcolumn = instance.nodeToRC[lastNode]
                if (curNode in instance.exits and step == nSteps):
                    continue
                cornerX, cornerY = self.computeXY(row, column)
                centerX, centerY = self.computeCenterXY(row, column)
                lcornerX, lcornerY = self.computeXY(lrow, lcolumn)
                lcenterX, lcenterY = self.computeCenterXY(lrow, lcolumn)
                stepX = (centerX - lcenterX)/nSteps
                stepY = (centerY - lcenterY)/nSteps
                create_circle(canvas, lcenterX + int(step*stepX), lcenterY + int(step*stepY), self.graphieSize/2, 
                              {'fill': self.instance.policies[i].color})
                if step == nSteps:
                    try:
                        self.drawDirection(curNode, self.directions[i][self.time])
                    except: pass
                canvas.create_text(lcenterX + int(step*stepX), lcenterY + int(step*stepY), text = str(i), fill="black", font = self.agentFont)
            self.drawExits(self.time if step == nSteps else self.lastTime)
            self.tk.update()
            self.tk.after(int(self.stepTime/(2*nSteps)))

    def run(self):
        self.tk.mainloop() 
        
def printPlan(instance, solution):
    for i, curPlan in enumerate(solution.paths):
        print("Agent", i, ":", end=" ")
        for node in curPlan:
            print(instance.nodeToRC[node], end="-->")
        print()
    
# Main program
def main():
    import instance
    import expandedNetwork
    import solveNetworkLIP
    import solution
    import simulation
    from policies import compliant
    from policies import nearestExit
    
    if sys.argv[1:]:
        inputFileName = sys.argv[1]
    else: # if running as script
        #inputFileName = '../instances/simplest.txt'
        #inputFileName = '../instances/two_lines.txt'
        inputFileName = '../instances/balancing.txt'
    timeThreshold = 20 
    instance = instance.Instance(inputFileName)
       
    network = expandedNetwork.ExpandedNetwork(instance, timeThreshold)
    print("Solving by MaxFlow (ignoring the hats)...")
    solution = solution.Solution(network.solveMaxFlow(), instance.exits) 
    solution.checkSolution(fixFlag = True)
    #printPlan(instance, simulation)
    solution.checkSolution()
    
    for i, policy in enumerate(instance.policies[:]):
        if policy == 'c': 
            instance.policies[i] = compliant.Compliant(solution.paths[i])
            continue
        if policy == 'n': 
            instance.policies[i] = \
            nearestExit.NearestExit(instance.graph, instance.exitDistances, instance.agents[i])
            continue
        print("An unknown policy " + str(policy))
        
    simulation = simulation.Simulation(instance, timeThreshold)


    print("Showing the simulation graphically...")    
    # Create the graphical objects...
    h = TkEvac(instance, simulation, nSteps = 20, stepTime = 500)
    h.run()

# Call main when run as script
if __name__ == '__main__':
    main() 
