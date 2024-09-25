from random import shuffle
import time
import pandas as pd
from fifteenpuzzle import *
from search import misplacedTilesHeuristic as h1, euclideanHeuristic as h2,\
    manhattanHeuristic as h3, tilesOutOfRowAndColHeuristic as h4, aStarSearch,\
    dfs, bfs, ucs

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
            "average maximum fringe size": sum(max_fringe_size[h_index]) / len(max_fringe_size[h_index]),
            "average tree depth": sum(depth[h_index]) / len(depth[h_index]),
            "average time": sum(execution_time[h_index]) / len(execution_time[h_index]),
            "average nodes used": sum(expanded_nodes[h_index]) / len(expanded_nodes[h_index])
        }
        summary.append(statistic)
        print(f"{heuristics[h_index].__name__}: ")
        print(statistic)
    nodes_list = [s['average tree depth'] for s in summary]
    fringe_size_list = [s['average maximum fringe size'] for s in summary]
    depth_list = [s['average time'] for s in summary]
    time_list = [s['average nodes used'] for s in summary]
    alg_names = [alg.__name__ for alg in heuristics]

    df = pd.DataFrame({
        "algorithm": alg_names,
        "average maximum fringe size": fringe_size_list,
        "average tree depth": nodes_list,
        "average time": depth_list,
        "average nodes used": time_list
    })
    df.set_index("algorithm")
    print(df)
    df.to_csv("./Heuristics.csv")

    best_h = heuristics[nodes_list.index(min(nodes_list))]
    print(f"The best heuristic found based on the number of generated nodes is: {best_h.__name__}")

def automate_uninformed_search_with_a_star(size=100, heuristic=h4):
    """
     This is a function that generates a list of random fifteenpuzzles of length size and solves
      them using dfs, bfs, ucs, and A* with the passed heuristic while keeping track of the average max
      fringe size,the average number of expanded nodes, the average max depth,
      and the average execution time.

      To save time and not investigate unsolvable puzzles. Only solvable initial states
      will get passed to the search algorithm
     """

    nonSolvableStates = 0
    max_fringe_size = [[0 for i in range(size)] for j in range(4)]
    expanded_nodes = [[0 for i in range(size)] for j in range(4)]
    depth = [[0 for i in range(size)] for j in range(4)]
    execution_time = [[0 for i in range(size)] for j in range(4)]

    def astarWithWrapper(problem):
        return aStarSearch(problem,heuristic)
    searchAlgorithms = [dfs, bfs, ucs, astarWithWrapper]

    permutaion = 0
    while permutaion < size:
        # if(permutaion%100==0):
        #     print(f"permutaion: {permutaion}")
        print(permutaion)
        puzzle = createRandomFifteenPuzzle(5)
        thisPuzzleIsSolvable = puzzle.isPossible()
        if (not thisPuzzleIsSolvable):
            nonSolvableStates += 1
            continue
        problem = FifteenPuzzleSearchProblem(puzzle)
        for h_index, alg in enumerate(searchAlgorithms):
            start = time.time_ns()
            actions, maxFringeSize, maxDepth, numberOfNodesExpanded = \
                alg(problem)
            end = time.time_ns()
            max_fringe_size[h_index][permutaion] = maxFringeSize
            depth[h_index][permutaion] = maxDepth
            expanded_nodes[h_index][permutaion] = numberOfNodesExpanded
            execution_time[h_index][permutaion] = (end - start) / (1e9)
        permutaion += 1

    summary = []
    for h_index in range(len(searchAlgorithms)):
        statistic = {
            "average maximum fringe size": sum(max_fringe_size[h_index]) / len(max_fringe_size[h_index]),
            "average tree depth": sum(depth[h_index]) / len(depth[h_index]),
            "average time": sum(execution_time[h_index]) / len(execution_time[h_index]),
            "average nodes used": sum(expanded_nodes[h_index]) / len(expanded_nodes[h_index])
        }
        summary.append(statistic)
        print(f"{searchAlgorithms[h_index].__name__}: ")
        print(statistic)
    nodes_list = [s['average tree depth'] for s in summary]
    fringe_size_list = [s['average maximum fringe size'] for s in summary]
    depth_list = [s['average time'] for s in summary]
    time_list = [s['average nodes used'] for s in summary]
    alg_names = [alg.__name__ for alg in searchAlgorithms]

    df = pd.DataFrame({
        "algorithm": alg_names,
        "average maximum fringe size": fringe_size_list,
        "average tree depth": nodes_list,
        "average time": depth_list,
        "average nodes used": time_list
    })
    df.set_index("algorithm")
    df.to_csv("./dfsAndTheRest.csv")
    print(df)
    best_h = searchAlgorithms[nodes_list.index(min(nodes_list))]
    print(f"The best heuristic found based on the number of generated nodes is: {best_h.__name__}")


# automate_heuristics_tests(size=100)
automate_uninformed_search_with_a_star()