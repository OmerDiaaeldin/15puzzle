from random import shuffle
import time
from fifteenpuzzle import *
from search import misplacedTilesHeuristic as h1, euclideanHeuristic as h2,\
    manhattanHeuristic as h3, tilesOutOfRowAndColHeuristic as h4, aStarSearch
def automate_heuristics_tests(size=100):
    """
    This is a function that generates a list of random fifteenpuzzles of length size and solves
     them using each one of the defined algorithms while keeping track of the average max
     fringe size,the average number of expanded nodes, the average max depth,
     and the average execution time.

     To save time and not investigate unsolvable puzzles. Only solvable initial states
     will get passed to the search algorithm. And for the sake of comparison the count of
     solvable states will be recorded
    """

    nonSolvableStates = 0
    max_fringe_size = [[0 for i in range(size)] for j in range(4)]
    expanded_nodes = [[0 for i in range(size)] for j in range(4)]
    depth = [[0 for i in range(size)]for j in range(4)]
    execution_time = [[0 for i in range(size)] for j in range(4)]
    heuristics = [h1,h2,h3,h4]


    permutaion = 0
    while permutaion < size:
        puzzle = createRandomFifteenPuzzle(20)
        thisPuzzleIsSolvable = puzzle.isPossible()
        if(not thisPuzzleIsSolvable):
            nonSolvableStates += 1
            continue
        problem = FifteenPuzzleSearchProblem(puzzle)
        for h_index, heuristic in enumerate(heuristics):
            start = time.time_ns()
            # print("h_index: ", h_index)
            # print(heuristic.__name__)
            actions, maxFringeSize, maxDepth, numberOfNodesExpanded = \
                aStarSearch(problem,heuristic)
            end = time.time_ns()
            max_fringe_size[h_index][permutaion] = maxFringeSize
            depth[h_index][permutaion] = maxDepth
            expanded_nodes[h_index][permutaion] = numberOfNodesExpanded
            execution_time[h_index][permutaion] = (end-start)/(1e9)
        permutaion += 1

    summary = []
    for h_index in range(len(heuristics)):
        statistic = {
            "f_size" : sum(max_fringe_size[h_index])/len(max_fringe_size[h_index]),
            "depth" : sum(depth[h_index])/len(depth[h_index]),
            "time" : sum(execution_time[h_index])/len(execution_time[h_index]),
            "nodes" : sum(expanded_nodes[h_index])/len(expanded_nodes[h_index])
        }
        summary.append(statistic)
        print(f"{heuristics[h_index].__name__}: ")
        print(statistic)
    nodes_list = [s['nodes'] for s in summary]
    best_h = heuristics[nodes_list.index(min(nodes_list))]
    print(f"The best heuristic found based on the number of generated nodes is: {best_h.__name__}")

automate_heuristics_tests(size=100)