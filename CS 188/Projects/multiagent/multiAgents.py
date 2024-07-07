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
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        if successorGameState.isWin():
            return float("inf")
        if successorGameState.isLose():
            return float("-inf")

        food_distance = []
        for food in newFood.asList():
            food_distance.append(manhattanDistance(newPos, food))

        ghost_distance = []
        newGhostPositions = successorGameState.getGhostPositions()
        for ghost in newGhostPositions:
            ghost_distance.append(manhattanDistance(newPos, ghost))
        if min(ghost_distance) <= 1:
            return float("-inf")

        return (
            successorGameState.getScore()
            + min(ghost_distance) / min(food_distance)
            + sum(newScaredTimes)
        )


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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
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

        def value(gameState, agentIndex, depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:
                return max_value(gameState, agentIndex, depth)
            else:
                return min_value(gameState, agentIndex, depth)

        def max_value(gameState, agentIndex, depth):
            v = -float("inf")
            for action in gameState.getLegalActions(agentIndex):
                v = max(
                    v, value(gameState.generateSuccessor(agentIndex, action), 1, depth)
                )
            return v

        def min_value(gameState, agentIndex, depth):
            v = float("inf")
            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    next_agentIndex = 0
                    next_depth = depth + 1
                else:
                    next_agentIndex = agentIndex + 1
                    next_depth = depth
                v = min(
                    v,
                    value(
                        gameState.generateSuccessor(agentIndex, action),
                        next_agentIndex,
                        next_depth,
                    ),
                )
            return v

        return max(
            gameState.getLegalActions(0),
            key=lambda a: value(gameState.generateSuccessor(0, a), 1, 0),
        )


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def value(gameState, agentIndex, depth, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:
                return max_value(gameState, agentIndex, depth, alpha, beta)
            else:
                return min_value(gameState, agentIndex, depth, alpha, beta)

        def max_value(gameState, agentIndex, depth, alpha, beta):
            v = -float("inf")
            for action in gameState.getLegalActions(agentIndex):
                v = max(
                    v,
                    value(
                        gameState.generateSuccessor(agentIndex, action),
                        1,
                        depth,
                        alpha,
                        beta,
                    ),
                )
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(gameState, agentIndex, depth, alpha, beta):
            v = float("inf")
            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    next_agentIndex = 0
                    next_depth = depth + 1
                else:
                    next_agentIndex = agentIndex + 1
                    next_depth = depth
                v = min(
                    v,
                    value(
                        gameState.generateSuccessor(agentIndex, action),
                        next_agentIndex,
                        next_depth,
                        alpha,
                        beta,
                    ),
                )
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        alpha = -float("inf")
        beta = float("inf")
        best_action = Directions.STOP
        for action in gameState.getLegalActions(0):
            v = value(gameState.generateSuccessor(0, action), 1, 0, alpha, beta)
            if v > alpha:
                best_action = action
                alpha = v
        return best_action


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

        def value(gameState, agentIndex, depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            if agentIndex == 0:
                return max_value(gameState, agentIndex, depth)
            else:
                return exp_value(gameState, agentIndex, depth)

        def max_value(gameState, agentIndex, depth):
            v = -float("inf")
            for action in gameState.getLegalActions(agentIndex):
                v = max(
                    v, value(gameState.generateSuccessor(agentIndex, action), 1, depth)
                )
            return v

        def exp_value(gameState, agentIndex, depth):
            v = 0
            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    next_agentIndex = 0
                    next_depth = depth + 1
                else:
                    next_agentIndex = agentIndex + 1
                    next_depth = depth
                v += value(
                    gameState.generateSuccessor(agentIndex, action),
                    next_agentIndex,
                    next_depth,
                ) / len(gameState.getLegalActions(agentIndex))
            return v

        return max(
            gameState.getLegalActions(0),
            key=lambda a: value(gameState.generateSuccessor(0, a), 1, 0),
        )


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")

    food_dist = []
    for food in currentGameState.getFood().asList():
        food_dist.append(manhattanDistance(currentGameState.getPacmanPosition(), food))

    ghost_dist = []
    for ghost in currentGameState.getGhostPositions():
        ghost_dist.append(
            manhattanDistance(currentGameState.getPacmanPosition(), ghost)
        )
    if min(ghost_dist) <= 1:
        return float("-inf")

    scared_times = [
        ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()
    ]

    return (
        currentGameState.getScore()
        + min(ghost_dist) / min(food_dist)
        - max(food_dist)
        + sum(scared_times)
    )


# Abbreviation
better = betterEvaluationFunction
