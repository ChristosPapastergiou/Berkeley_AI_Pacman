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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
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

    def getCostOfActions(self, Actions):
        """
         Actions: A list of Actions to take

        This method returns the total cost of a particular sequence of Actions.
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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first
    """

    "*** YOUR CODE HERE ***"
    
    Expanded = set()
    Frontier = util.Stack()              # For this algorithm we need a stack (Depth first)
    Frontier.push((problem.getStartState(), []))     

    while not Frontier.isEmpty():        # Search all the Queue until it is empty
        State, Actions = Frontier.pop()  # Pop it and save the data

        if problem.isGoalState(State):  # Found goal state? return the path list
            return Actions

        if State not in Expanded:        # Visit the state (node) we are in in case we didnt before
            Expanded.add(State)

            for state, action, _ in problem.getSuccessors(State):   # We dont need the cost for this algorithm 
                Frontier.push((state, Actions + [action]))          # Total actions = all previous + the action we did right now

    return None       # Return failure

def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first
    """

    "*** YOUR CODE HERE ***"

    # Same as DFS but for this algorithm we need a queue (Width first)

    Expanded = set()
    Frontier = util.Queue()
    Frontier.push((problem.getStartState(), []))

    while not Frontier.isEmpty():
        State, Actions = Frontier.pop()

        if problem.isGoalState(State):
            return Actions

        if State not in Expanded:
            Expanded.add(State)

            for state, action, _ in problem.getSuccessors(State):            
                Frontier.push((state, Actions + [action]))

    return None

def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first
    """

    "*** YOUR CODE HERE ***"

    # Same as DFS & BFS but for this algorithm we need a priority queue cause we need the cost of action

    Expanded = set()
    Frontier = util.PriorityQueue()      
    Frontier.push((problem.getStartState(), [], 0), 0) 

    while not Frontier.isEmpty():
        State, Actions, Cost = Frontier.pop()

        if problem.isGoalState(State):
            return Actions

        if State not in Expanded:
            Expanded.add(State)

            for state, action, cost in problem.getSuccessors(State):
                Frontier.push((state, Actions + [action], Cost + cost), Cost + cost) # Priority is the total amount of cost so far

    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    "*** YOUR CODE HERE ***"

    # Same as UCS but for this algorithm we need to add the heuristic cost
    
    Expanded = set()
    Frontier = util.PriorityQueue()      
    Frontier.push((problem.getStartState(), [], 0), 0) 

    while not Frontier.isEmpty():
        State, Actions, Cost = Frontier.pop()

        if problem.isGoalState(State):
            return Actions

        if State not in Expanded:
            Expanded.add(State)

            for state, action, cost in problem.getSuccessors(State):
                Frontier.push((state, Actions + [action], Cost + cost), Cost + cost + heuristic(state, problem))    # We also need the heuristic

    return None

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
