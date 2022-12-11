from concorde.tsp import TSPSolver
from concorde.tests.data_utils import get_dataset_path
fname = get_dataset_path("/Users/tok/PycharmProjects/tsp2/problem_explicit")

# fname = get_dataset_path("/Users/tok/PycharmProjects/tsp2/problem_explicit")
solver = TSPSolver.from_tspfile(fname)
print(solver)
solution = solver.solve(verbose=True)
print(solution)
