# eightpuzzle.py
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


import search
import random

# Module Classes

#/*=====Start Change Task 1=====*/
class FifteenPuzzleState:
    """
    The Fifteen Puzzle is described in the course textbook on
    page 64.

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the FifteenPuzzleSearchProblem class.
    """

    # *=====End Change Task 1 =====*/
    def __init__( self, numbers ):
        """
          Constructs a new fifteen puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 15 representing an
          instance of the eight puzzle.  15 represents the blank
          space.  Thus, the list

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:] # Make a copy so as not to cause side-effects.
        numbers.reverse()
        # /*=====Start Change Task 1=====*/
        for row in range( 4 ):
            self.cells.append( [] )
            for col in range( 4 ):
                self.cells[row].append( numbers.pop() )
                if self.cells[row][col] == 15:
                    # /*=====End Change Task 1=====*/
                    self.blankLocation = row, col

    def isGoal( self ):
        current = 0
        # /*=====Start Change Task 1=====*/
        for row in range( 4 ):
            for col in range( 4 ):
                # /*=====End Change Task 1=====*/
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        """
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        # /*=====Start Change Task 1=====*/
        if(row != 3):
            # /*=====End Change Task 1=====*/
            moves.append('down')
        if(col != 0):
            moves.append('left')
        # /*=====Start Change Task 1=====*/
        if(col != 3):
            # /*=====End Change Task 1=====*/
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new FifteenPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current eightPuzzle
        # /*=====Start Change Task 1=====*/
        newPuzzle = FifteenPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # /*=====End Change Task 1=====*/
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # /*=====Start Change Task 3=====*/
    def isPossible(self):
        """
        This is a method that checks whether a certain puzzle is
        possible or not based on a simple algorithm. The puzzle is solvable if
        and only if the parity of the number of inversions (ignoring the blank space)
        is different than the parity of the row of the blank cell (0 indexing)
        """
        inversions = 0
        blank_space_row = 0
        flattenedState = []
        for i in range(4):
            for j in range(4):
                if(self.cells[i][j] == 15):
                    blank_space_row = i
                else:
                    flattenedState.append(self.cells[i][j])

        for i in range(15):
            for j in range(i+1,15):
                if(flattenedState[j] < flattenedState[i]):
                    inversions += 1
        if(inversions %2 != blank_space_row%2):
            return True
        else:
            return False
    # /*=====End Change Task 3=====*/

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two FifteenPuzzles with the same configuration
          are equal.

        """
        # /*=====Start Change Task 1=====*/
        for row in range( 4 ):
            # /*=====End Change Task 1=====*/
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (13))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                # /*=====Start Change Task 1=====*/
                col = col+1
                if col == 16:
                    # /*=====End Change Task 1=====*/
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class
#/*=====Start Change Task 1=====*/
class FifteenPuzzleSearchProblem(search.SearchProblem):
    # /*=====End Change Task 1=====*/
    """
      Implementation of a SearchProblem for the  Fifteen Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self,puzzle):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self,state):
        return state.isGoal()

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

# def loadFifteenPuzzle(puzzleNumber):
#     """
#       puzzleNumber: The number of the Fifteen puzzle to load.
#
#       Returns an Fifteen puzzle object generated from one of the
#       provided puzzles in Fifteen_PUZZLE_DATA.
#
#       puzzleNumber can range from 0 to 5.
#
#     """
#     return EightPuzzleState(EIGHT_PUZZLE_DATA[puzzleNumber])
#
def createRandomFifteenPuzzle(moves=100):
    """
      moves: number of random moves to apply

      Creates a random 15 puzzle by applying
      a series of 'moves' random moves to a solved
      puzzle.
    """
    puzzle = FifteenPuzzleState([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

if __name__ == '__main__':
    puzzle = createRandomFifteenPuzzle(25)
    print('A random puzzle:')
    print(puzzle)

    problem = FifteenPuzzleSearchProblem(puzzle)
    heuristic = search.h4
    path= search.aStarSearch(problem, heuristic)
    """
    path = search.breadthFirstSearch(problem)
    """   
    print('A* found a path of %d moves: %s' % (len(path), str(path)))
    curr = puzzle
    i = 1
    for a in path[0]:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)

        input("Press return for the next state...")   # wait for key stroke
        i += 1
