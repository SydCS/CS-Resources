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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    cur = (problem.getStartState(), [])  # state, path
    fringe = util.Stack()  # DFS
    fringe.push(cur)
    visited = set()

    while not fringe.isEmpty():
        cur = fringe.pop()
        if problem.isGoalState(cur[0]):
            return cur[1]
        if cur[0] not in visited:
            visited.add(cur[0])
            for successor in problem.getSuccessors(cur[0]):
                fringe.push((successor[0], cur[1] + [successor[1]]))

    return cur[1]


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    cur = (problem.getStartState(), [])  # state, path
    fringe = util.Queue()  # BFS
    fringe.push(cur)
    visited = set()

    while not fringe.isEmpty():
        cur = fringe.pop()
        if problem.isGoalState(cur[0]):
            return cur[1]
        if cur[0] not in visited:
            visited.add(cur[0])
            for successor in problem.getSuccessors(cur[0]):
                fringe.push((successor[0], cur[1] + [successor[1]]))

    return cur[1]


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    cur = (problem.getStartState(), [], 0)  # state, path, cost
    fringe = util.PriorityQueueWithFunction(lambda n: n[2])  # UCS
    fringe.push(cur)
    visited = set()

    while not fringe.isEmpty():
        cur = fringe.pop()
        if problem.isGoalState(cur[0]):
            return cur[1]
        if cur[0] not in visited:
            visited.add(cur[0])
            for successor in problem.getSuccessors(cur[0]):
                fringe.push(
                    (
                        successor[0],
                        cur[1] + [successor[1]],
                        cur[2] + successor[2],
                    )
                )

    return cur[1]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = (problem.getStartState(), [], 0)
    fringe = util.PriorityQueue()  # A*
    fringe.push(start, heuristic(problem.getStartState(), problem))
    visited = set()

    while not fringe.isEmpty():
        (state, path, cost) = fringe.pop()
        if problem.isGoalState(state):
            return path
        if state not in visited:
            visited.add(state)
            for next_state, next_action, next_cost in problem.getSuccessors(state):
                fringe.push(
                    (
                        next_state,
                        path + [next_action],
                        cost + next_cost,
                    ),
                    cost + next_cost + heuristic(next_state, problem),
                )

    return start[1]


def genericSearch(problem, fringe, policy):
    """
    A generic search function that can be used for different search strategies.

    :param problem: The search problem instance.
    :param fringe: The data structure used to store nodes.
    :param policy: A function to add successors to the fringe. This function should take the fringe, successors, and current path as arguments.
    """

    pass


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
