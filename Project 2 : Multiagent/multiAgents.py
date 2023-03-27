# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        if currentGameState.isWin():
            return float("inf")
        elif currentGameState.isLose():
            return -float("inf")

        ClosestFood = float("inf")
        for food in newFood.asList():
            ClosestFood = min(ClosestFood, manhattanDistance(newPos, food)) # Taking the closest food to pacman using manhattan

        for ghost in successorGameState.getGhostPositions():
            if (manhattanDistance(newPos, ghost) <= 1):           # If there is a ghost too close to pacman then give a really low value to change direction
                return -float("inf")

        return successorGameState.getScore() + 1.0/ClosestFood

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        NumberOfAgents = gameState.getNumAgents()

        def MinimaxDecision(gameState):
            value = -float("inf")
            for action in gameState.getLegalActions(0):
                NextState = gameState.generateSuccessor(0, action)
                NewValue = MinValue(NextState, 0, 1)

                if NewValue > value:
                    value = NewValue
                    TheAction = action

            return TheAction

        def MaxValue(gameState, depth, agentIndex):
            if gameState.isLose() or gameState.isWin() or self.depth == depth:  # Not only the depth, we need to check if we won or lost the game too
                return self.evaluationFunction(gameState)

            value = -float("inf")
            for action in gameState.getLegalActions(agentIndex):
                value = max(value, MinValue(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1))

            return value

        def MinValue(gameState, depth, agentIndex):
            if gameState.isLose() or gameState.isWin() or self.depth == depth:  # Not only the depth, we need to check if we won or lost the game too
                return self.evaluationFunction(gameState)

            value = float("inf")
            if NumberOfAgents - 1 == agentIndex:                                                                            # Need to have two cases here because pacman is max player
                for action in gameState.getLegalActions(agentIndex):                                                        # but ghosts are min players. So 1st will be the pacman 2nd 
                    value = min(value, MaxValue(gameState.generateSuccessor(agentIndex, action), depth + 1, 0))             # a ghost 3rd another ghost 4th another ghost etc until all ghost
            else:                                                                                                           # are done. Whenever pacman has the turn again depth will be increased
                for action in gameState.getLegalActions(agentIndex):                                                        # because all players are done with their move. Lastly checking if it
                    value = min(value, MinValue(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1))    # is pacman's turn by checking agents's index. Pacman's index = 0

            return value

        return MinimaxDecision(gameState)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # Like minimax algorithm but we need to use also alpha and beta values

        NumberOfAgents = gameState.getNumAgents()
        
        def AlphaBetaSearch(gameState):
            value = -float("inf")
            alpha = -float("inf")
            beta = float("inf")
            for action in gameState.getLegalActions(0):
                NextState = gameState.generateSuccessor(0, action)
                NewValue = MinValue(NextState, 0, 1, alpha, beta)

                if NewValue > value:
                    value = NewValue
                    TheAction = action

                alpha = max(alpha, value)

            return TheAction

        def MaxValue(gameState, depth, agentIndex, alpha, beta):
            if gameState.isLose() or gameState.isWin() or self.depth == depth:  # Not only the depth, we need to check if we won or lost the game too
                return self.evaluationFunction(gameState)

            value = -float("inf")
            for action in gameState.getLegalActions(agentIndex):
                value = max(value, MinValue(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta))

                if value > beta:
                    return value

                alpha = max(alpha, value)

            return value

        def MinValue(gameState, depth, agentIndex, alpha, beta):
            if gameState.isLose() or gameState.isWin() or self.depth == depth:  # Not only the depth, we need to check if we won or lost the game too
                return self.evaluationFunction(gameState)

            value = float("inf")
            if NumberOfAgents - 1 == agentIndex:
                for action in gameState.getLegalActions(agentIndex):
                    value = min(value, MaxValue(gameState.generateSuccessor(agentIndex, action), depth + 1, 0, alpha, beta))

                    if value < alpha:
                        return value

                    beta = min(beta, value)
            else:
                for action in gameState.getLegalActions(agentIndex):
                    value = min(value, MinValue(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)) 

                    if value < alpha:
                        return value

                    beta = min(beta, value)

            return value

        return AlphaBetaSearch(gameState)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        # Like minimax but insted of minimum we need to take average value for the ghosts. 
        
        NumberOfAgents = gameState.getNumAgents()

        def ExpectimaxDecision(gameState):
            value = -float("inf")
            for action in gameState.getLegalActions(0):
                NextState = gameState.generateSuccessor(0, action)
                NewValue = ExpectValue(NextState, 0, 1)

                if NewValue > value:
                    value = NewValue
                    TheAction = action

            return TheAction

        def MaxValue(gameState, depth, agentIndex):
            if gameState.isLose() or gameState.isWin() or self.depth == depth:  # Not only the depth, we need to check if we won or lost the game too
                return self.evaluationFunction(gameState)

            value = -float("inf")
            for action in gameState.getLegalActions(agentIndex):
                value = max(value, ExpectValue(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1))

            return value

        def ExpectValue(gameState, depth, agentIndex):
            if gameState.isLose() or gameState.isWin() or self.depth == depth:  # Not only the depth, we need to check if we won or lost the game too
                return self.evaluationFunction(gameState)

            Total = 0
            TotalValue = 0
            value = float("inf")
            if NumberOfAgents - 1 == agentIndex:
                for action in gameState.getLegalActions(agentIndex):                                                # Taking the average value whenever it is ghost's
                    value = MaxValue(gameState.generateSuccessor(agentIndex, action), depth + 1, 0)                 # turn. This is useful for modeling probabilistic 
                    Total += value                                                                                  # behavior of agents who may make suboptimal choices.
                    TotalValue = Total/len(gameState.getLegalActions(agentIndex))                                   # Although whenever it is pacman's turn we need the 
            else:                                                                                                   # optimal choice so we do not need to calculate
                for action in gameState.getLegalActions(agentIndex):                                                # the average value. Again like minimax and alphabeta
                    value = ExpectValue(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)     # it will be pacman's turn whenever all ghosts are done
                    Total += value                                                                                  # with their move. Pacman's index = 0
                    TotalValue = Total/len(gameState.getLegalActions(agentIndex))

            return TotalValue

        return ExpectimaxDecision(gameState)

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Eat the nearest food and if a capsule is near you eat it 
    and then eat the scared ghost because the final score will be bigger.
    
    """
    "*** YOUR CODE HERE ***"

    TotalScore = 0
    Food = currentGameState.getFood()
    Capsules = currentGameState.getCapsules()
    GhostState = currentGameState.getGhostStates()
    PacmanPosition = currentGameState.getPacmanPosition() 

    if currentGameState.isWin():
        return float("inf")
    elif currentGameState.isLose():
        return -float("inf")

    ClosestFood = float("inf")
    for food in Food.asList():
        ClosestFood = min(ClosestFood, manhattanDistance(PacmanPosition, food)) # Taking the closest food to pacman using manhattan

    for capsule in Capsules:
        if (manhattanDistance(PacmanPosition, capsule) <= 2):   # If pacman is near to a capsule i give higher score because i want to eat it 
            TotalScore += 100

    for ghost in GhostState:
        if ghost.scaredTimer:   # If the ghost is scared eat because the score will be higher
            TotalScore += 100

    return currentGameState.getScore() + 1.0/ClosestFood + TotalScore   

# Abbreviation
better = betterEvaluationFunction
