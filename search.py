# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, we implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem,max_depth=1000):
    """Search the deepest nodes in the search tree first."""

    #states to be explored (LIFO). holds nodes in form (state, action)
    frontier = util.Stack()
    #previously explored states (for path checking), holds states
    exploredNodes = []
    #define start node
    startState = problem.getStartState()

    # /*=====Start Change Task 4=====*/
    startNode = (startState, [], 0) #(state, action, depth)
    maxFringeSize = 1 # currently only the start state
    maxDepth = 0 # the current depth is 0
    numberOfNodesExpanded = 1 # only the root node
    # /*=====End Change Task 4=====*/
    
    frontier.push(startNode)
    
    while not frontier.isEmpty():
        #begin exploring last (most-recently-pushed) node on frontier
        # /*=====Start Change Task 4=====*/
        currentState, actions, currentDepth = frontier.pop()

        # /*=====End Change Task 4=====*/
        
        if currentState not in exploredNodes:
            #mark current node as explored
            exploredNodes.append(currentState)

            if problem.isGoalState(currentState):
                # /*=====Start Change Task 4=====*/
                return (actions, maxFringeSize, maxDepth, numberOfNodesExpanded)
                # /*=====End Change Task 4=====*/
            else:
                #get list of possible successor nodes in 
                #form (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                #push each successor to frontier
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    # /*=====Start Change Task 4=====*/
                    newDepth = currentDepth + 1
                    newNode = (succState, newAction, newDepth)
                    if(newDepth > max_depth):
                        continue
                    # /*=====End Change Task 4=====*/
                    frontier.push(newNode)
                    # /*=====Start Change Task 4=====*/
                    maxFringeSize = max(maxFringeSize, len(frontier))
                    numberOfNodesExpanded += 1
                    maxDepth = max(maxDepth, newDepth)
                    # /*=====End Change Task 4=====*/

    # /*=====Start Change Task 4=====*/
    return (actions, maxFringeSize, maxDepth, numberOfNodesExpanded)
    # /*=====End Change Task 4=====*/

def breadthFirstSearch(problem,max_depth=1000):
    """Search the shallowest nodes in the search tree first."""

    #to be explored (FIFO)
    frontier = util.Queue()
    
    #previously expanded states (for cycle checking), holds states
    exploredNodes = []
    
    startState = problem.getStartState()
    # /*=====Start Change Task 4=====*/
    startNode = (startState, [], 0) #(state, action, depth)
    maxFringeSize = 1 # currently only the start state
    maxDepth = 0 # the current depth is 0
    numberOfNodesExpanded = 1 # only the root node
    # /*=====End Change Task 4=====*/
    
    frontier.push(startNode)
    
    while not frontier.isEmpty():
        #begin exploring first (earliest-pushed) node on frontier
        currentState, actions, currentDepth = frontier.pop()
        
        if currentState not in exploredNodes:
            #put popped node state into explored list
            exploredNodes.append(currentState)

            if problem.isGoalState(currentState):
                return (actions, maxFringeSize, maxDepth, numberOfNodesExpanded)
            else:
                #list of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    # /*=====Start Change Task 4=====*/
                    newDepth = currentDepth + 1
                    newNode = (succState, newAction, newDepth)
                    if (newDepth > max_depth):
                        continue
                    # /*=====End Change Task 4=====*/

                    frontier.push(newNode)
                    # /*=====Start Change Task 4=====*/
                    maxFringeSize = max(maxFringeSize, len(frontier))
                    numberOfNodesExpanded += 1
                    maxDepth = max(maxDepth, newDepth)
                    # /*=====End Change Task 4=====*/

    # /*=====Start Change Task 4=====*/
    return (actions, maxFringeSize, maxDepth, numberOfNodesExpanded)
    # /*=====End Change Task 4=====*/

def uniformCostSearch(problem, max_depth=1000):
    """Search the node of least total cost first."""

    #to be explored (FIFO): holds (item, cost)
    frontier = util.PriorityQueue()

    #previously expanded states (for cycle checking), holds state:cost
    exploredNodes = {}
    
    startState = problem.getStartState()
    # /*=====Start Change Task 4=====*/
    startNode = (startState, [], 0, 0)  # (state, action, cost, depth)
    maxFringeSize = 1  # currently only the start state
    maxDepth = 0  # the current depth is 0
    numberOfNodesExpanded = 1  # only the root node
    # /*=====End Change Task 4=====*/
    
    frontier.push(startNode, 0)
    
    while not frontier.isEmpty():
        #begin exploring first (lowest-cost) node on frontier
        currentState, actions, currentCost, currentDepth = frontier.pop()
       
        if (currentState not in exploredNodes) or (currentCost < exploredNodes[currentState]):
            #put popped node's state into explored list
            exploredNodes[currentState] = currentCost

            if problem.isGoalState(currentState):
                return (actions, maxFringeSize, maxDepth, numberOfNodesExpanded)
            else:
                #list of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    # /*=====Start Change Task 4=====*/
                    newDepth = currentDepth + 1
                    newNode = (succState, newAction, newCost, newDepth)
                    if (newDepth > max_depth):
                        continue
                    # /*=====End Change Task 4=====*/

                    frontier.update(newNode, newCost)
                    # /*=====Start Change Task 4=====*/
                    maxFringeSize = max(maxFringeSize, len(frontier))
                    numberOfNodesExpanded += 1
                    maxDepth = max(maxDepth, newDepth)
                    # /*=====End Change Task 4=====*/

    # /*=====Start Change Task 4=====*/
    return (actions, maxFringeSize, maxDepth, numberOfNodesExpanded)
    # /*=====End Change Task 4=====*/


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
#/*=====Start Change Task 2=====*/

def misplacedTilesHeuristic(state, problem=None):
    """
    This heuristic function takes a state and estimates the cost to the nearest
    goal as equal to the number of misplaced tiles
    """
    current = 0
    misplaced_tile_count = 0
    for row in state.cells:
        for col in row:
            if(col != current):
                misplaced_tile_count += 1
            current += 1
    return misplaced_tile_count

def euclideanHeuristic(state, problem=None):
    total_distance = 0
    for (row_count,row) in enumerate(state.cells):
        for (col_count,col) in enumerate(row):
            # get the final position of this value
            eventual_row, eventual_col = util.getFinalPosition(col)
            total_distance += util.euclideanDistance((eventual_row, eventual_col),(row_count,col_count))
    return total_distance
def manhattanHeuristic(state, problem=None):
    total_distance = 0
    for (row_count, row) in enumerate(state.cells):
        for (col_count, col) in enumerate(row):
            # get the final position of this value
            if(col == 15):
                continue
            eventual_row, eventual_col = util.getFinalPosition(col)
            total_distance += util.manhattanDistance((eventual_row, eventual_col), (row_count, col_count))
    # print(state)
    # print(total_distance)
    return total_distance
def tilesOutOfRowAndColHeuristic(state, problem=None):
    total_estimated_cost = 0
    for (row_count, row) in enumerate(state.cells):
        for (col_count, col) in enumerate(row):
            # get the final position of this value
            eventual_row, eventual_col = util.getFinalPosition(col)
            if(eventual_row != row_count):
                total_estimated_cost += 1
            if(eventual_col != col_count):
                total_estimated_cost += 1
    return total_estimated_cost


#/*=====End Change Task 2=====*/
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    #to be explored (FIFO): takes in item, cost+heuristic
    frontier = util.PriorityQueue()

    exploredNodes = [] #holds (state, cost)

    startState = problem.getStartState()
    # /*=====Start Change Task 3=====*/
    startNode = (startState, [], 0, 0) #(state, action, cost, depth)
    maxFringeSize = 1 # currently only the start state
    maxDepth = 0 # the current depth is 0
    numberOfNodesExpanded = 1 # only the root node
    # /*=====End Change Task 3=====*/

    frontier.push(startNode, 0)

    while not frontier.isEmpty():

        #begin exploring first (lowest-combined (cost+heuristic) ) node on frontier

        # /*=====Start Change Task 3=====*/
        currentState, actions, currentCost, currentDepth = frontier.pop()

        # /*=====End Change Task 3=====*/

        #put popped node into explored list
        currentNode = (currentState, currentCost)
        exploredNodes.append((currentState, currentCost))

        if problem.isGoalState(currentState):
            # /*=====Start Change Task 3=====*/
            return (actions,maxFringeSize,maxDepth,numberOfNodesExpanded)
            # /*=====End Change Task 3=====*/

        else:
            #list of (successor, action, stepCost)
            successors = problem.getSuccessors(currentState)

            #examine each successor
            for succState, succAction, succCost in successors:
                newAction = actions + [succAction]
                newCost = problem.getCostOfActions(newAction)
                # /*=====Start Change Task 3=====*/
                newDepth = currentDepth + 1
                newNode = (succState, newAction, newCost, newDepth)
                # /*=====End Change Task 3=====*/
                #check if this successor has been explored
                already_explored = False
                for explored in exploredNodes:
                    #examine each explored node tuple
                    exploredState, exploredCost = explored

                    if (succState == exploredState) and (newCost >= exploredCost):
                        already_explored = True

                #if this successor not explored, put on frontier and explored list
                if not already_explored:
                    frontier.push(newNode, newCost + heuristic(succState, problem))
                    exploredNodes.append((succState, newCost))
                    # /*=====Start Change Task 3=====*/
                    maxFringeSize = max(maxFringeSize,len(frontier))
                    numberOfNodesExpanded += 1
                    maxDepth = max(maxDepth,newDepth)
                    # /*=====End Change Task 3=====*/
        # /*=====Start Change Task 3=====*/
    return (actions,maxFringeSize,maxDepth,numberOfNodesExpanded)
    # /*=====End Change Task 3=====*/


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
