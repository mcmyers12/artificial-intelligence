import copy


class Node:
    def __init__(self):
        self.state = []
        self.parentStates = []
        self.fCost = 0
        self.gCost = 0

class Solver:

    def __init__(self, startingState):
        self.goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        
        #Create the starting state as a node initialized with given startingState
        self.startingState = Node()
        self.startingState.state = startingState
        self.startingState.parentStates = []
        self.startingState.fCost = 0
        
        #self.openList = []
        #self.closedList = []
    
    
    def initializeAStar(self):
        #Add the starting state to the open list
        openList = []
        closedList = []
        openList.append(self.startingState) 
        
        #Find all adjacent states 
        adjacentStates = self.getAdjacentStates(self.startingState.state)
        
        #Add states to open list
        for state in adjacentStates:
            #Save starting state as a parent
            state.parentStates.append(self.startingState.state)
            
            #Calculate fCost of state
            state.fCost, state.gCost = self.calculateFCost(state)
            
            self.insertIntoOpenList(state, openList)
            
        #Remove the starting state from the open list, add it to the closed list
        openList.pop(openList.index(self.startingState))
        closedList.append(self.startingState)
        
        print 'Open List: '
        for i in openList:
            print '    state: ', i.state
            print '    parentStates: ', i.parentStates
            print '    fCost: ', i.fCost
            print '    gCost: ', i.gCost
            print
            
        print 'Closed List: '
        for i in closedList:
            print '    state: ', i.state
            print '    parentStates: ', i.parentStates
            print '    fCost: ', i.fCost
            print '    gCost: ', i.gCost
            print
            
        closedList = self.aStarAlgorithm(openList, closedList)
        self.printPath(closedList)

            
    
    def aStarAlgorithm(self, openList, closedList):
        '''Implements the A Star algorithm.'''
        #Base case: target state is in the closed list
        for node in closedList:
            if node.state == self.goal:
                print 'Goal State Found'
                return closedList
         
        #Choose the state from the open list with the lowest f cost
        lowestFState = openList[0]
        #Remove from the open list, add it to the closed list
        openList.pop(openList.index(lowestFState))
        closedList.append(lowestFState)
         
        #Get adjacent states, add them to the open list, if not on the open list already
        #Make the previous state the parent of all the adjacent states
        adjacentStates = self.getAdjacentStates(lowestFState.state)
        for state in adjacentStates:     
            #If the state is on the closed list, ignore it
            if self.checkIfStateInClosedList(state, closedList):
                print
                print 'already CLOSED list'
                print
                pass
            
            #If it isn't in the open list, add it, update parent and cost
            elif not self.checkIfStateInOpenList(state, openList):                
                print
                print 'NOT in open list'
                print
            
                #Make the previous state the parent
                state.parentStates.append(lowestFState.state)
            
                #Calculate fCost of state
                state.fCost, state.gCost = self.calculateFCost(state)

                print '    state: ', state.state
                print '    parentStates: ', state.parentStates
                print '    fCost: ', state.fCost
                print '    gCost: ', state.gCost
                print
                
                self.insertIntoOpenList(state, openList)
            
            #If the state is already in the open list, check to see if the G score for that 
                #state is lower if we use the current state to get there.  If the G cost is 
                #lower, change the state's parent to the previous square and recalculate its 
                #F and G costs, if not, don't change its parent. 
            elif self.checkIfStateInOpenList(state, openList):
                print 'ALREADY in open list'
                #Make the previous state the parent
                state.parentStates.append(lowestFState.state)
            
                #Calculate fCost, gCost of state
                state.fCost, currentGCost = self.calculateFCost(state)
                print 'Current gCost: ', currentGCost
                
                #Get the gCost of the state in the open list                
                openListGCost = self.getGCostInOpenList(state.state, openList)
                print 'OpenList gCost: ', openListGCost
                
                #If the current gCost is lower, update the state in the open list
                if currentGCost < openListGCost:
                    #Remove the old state
                    openList.pop(openList.index(state))
                    #Insert the updated state
                    self.insertIntoOpenList(state, openList)
               
        self.aStarAlgorithm(openList, closedList)
        
    
    
    def getGCostInOpenList(self, state, openList):
        '''Find the given state in the open list and get its gCost.'''
        for node in openList:
            if node.state == state:
                return node.gCost    
      
        
    def checkIfStateInClosedList(self, stateToCheck, closedList):
        for node in closedList:
            if node.state == stateToCheck.state:
                return True
        return False
    
        
    def checkIfStateInOpenList(self, stateToCheck, openList):
        for node in openList:
            if node.state == stateToCheck.state:
                return True
        return False
    
    
    def calculateFCost(self, currentState):
        '''Calculates the F Cost of the current state.'''
        #G cost is the number of parents aka number of steps taken from initial state
        gCost = len(currentState.parentStates)
                
        #Define H cost goal state
        hCostGoal = {0: (0,0), 1: (0,1), 2: (0,2), 3: (1,0), 4: (1,1), 5: (1,2), 6: (2,0), 7: (2,1), 8: (2,2)}
        
        #Convert state into a dictionary with coordinate pairs
        newState = []
        row1 = [currentState.state[0], currentState.state[1], currentState.state[2]]
        row2 = [currentState.state[3], currentState.state[4], currentState.state[5]]
        row3 = [currentState.state[6], currentState.state[7], currentState.state[8]]
        newState.append(row1)
        newState.append(row2)
        newState.append(row3)
        
        stateCoordDictionary = {}
        for x,row in enumerate(newState):
            for y,value in enumerate(row):
                stateCoordDictionary[value] = (x,y)
        
        #Calculate the manhattan distance
        hCost = 0
        for square in stateCoordDictionary:
            x = stateCoordDictionary[square][0]
            y = stateCoordDictionary[square][1]
            xGoal = hCostGoal[square][0]
            yGoal = hCostGoal[square][1]
            distance = abs(x - xGoal) + abs(y - yGoal)
            hCost += distance
            
        fCost = gCost + hCost
        return fCost, gCost
        
        
    def getGoalState(self, closedList):
        '''Gets the information about the goal state once it is in the closed list.'''
        for node in closedList:
            if node.state == self.goal:
                return node
        
        
    def printPath(self, closedList):
        #Get the end goal node from the closed list, which has the info we want
        pathToGoal = self.getGoalState(closedList)
        
        #Print the list of parent states of the node
        for state in pathToGoal.parentStates:
            print state
            
    
    def insertIntoOpenList(self, node, openList):
        openList.append(node)
        openList.sort(key=lambda x: x.fCost)
        
    
    #TODO THIS IS THE PART I'M UNSURE ABOUT
    def createNewState(self, zeroIndex, itemToSwapIndex, currentState):
        '''Creates an adjacent state and returns it as a node.'''
        #newState = copy.deepcopy(currentState)
        newState = currentState[:]
        temp = newState[zeroIndex]
        newState[zeroIndex] = newState[itemToSwapIndex]
        newState[itemToSwapIndex] = temp
        
        node = Node()
        node.state = newState
        node.parentStates = []
        node.fCost = 0
        
        return node
    
    
    def getAdjacentStates(self, currentState):
        '''Returns a list of all adjacent states.'''
        zeroLocation = currentState.index(0)
        
        adjacentStates = []
        
        if zeroLocation == 0:
            newState = self.createNewState(zeroLocation, 1, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 3, currentState)
            adjacentStates.append(newState)
        
        elif zeroLocation == 1:
            newState = self.createNewState(zeroLocation, 0, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 2, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 4, currentState)
            adjacentStates.append(newState)

        elif zeroLocation == 2:
            newState = self.createNewState(zeroLocation, 1, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 5, currentState)
            adjacentStates.append(newState)
  
        elif zeroLocation == 3:
            newState = self.createNewState(zeroLocation, 0, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 4, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 6, currentState)
            adjacentStates.append(newState)
            
        elif zeroLocation == 4:
            newState = self.createNewState(zeroLocation, 1, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 3, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 5, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 7, currentState)
            adjacentStates.append(newState)
            
        elif zeroLocation == 5:
            newState = self.createNewState(zeroLocation, 2, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 4, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 8, currentState)
            adjacentStates.append(newState)
            
        elif zeroLocation == 6:
            newState = self.createNewState(zeroLocation, 3, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 7, currentState)
            adjacentStates.append(newState)
        
        elif zeroLocation == 7:
            newState = self.createNewState(zeroLocation, 6, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 4, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 8, currentState)
            adjacentStates.append(newState) 
            
        elif zeroLocation == 8:
            newState = self.createNewState(zeroLocation, 5, currentState)
            adjacentStates.append(newState)
            newState = self.createNewState(zeroLocation, 7, currentState)
            adjacentStates.append(newState) 
            
        
        return adjacentStates
            
        
        
def main():
    s = Solver([1,0,2,3,5,4,6,7,8])
    s.initializeAStar()
    

main()