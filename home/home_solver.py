from home.home_game import Home
from home.home_strategy import HomeStrategy

import solve.framework as framework
from solve.decoupled_predictor import DecoupledPredictor
from solve.solver_data import SolverData
from solve.solver import Solver
from solve.plotter import Plotter
from solve.dqn import DQN

game = Home()
framework.load_game_data(game)

solverData = SolverData()
solverData['NUM_EPOCHS'] = 600

strategy = HomeStrategy(game)
solver = Solver(framework, DecoupledPredictor(DQN), solverData, strategy)

Plotter(solver.execute(), solverData)