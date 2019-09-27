from cia.cia_game import CIA
from cia.cia_strategy import CIAStrategy
import solve.framework as framework
from solve.decoupled_predictor import DecoupledPredictor
from solve.coupled_predictor import ModelPerVerbPredictor, ModelPerActionPredictor, ModelPerObjectPredictor
from solve.dqn import DQN, DQNStacked
from solve.solver_data import SolverData
from solve.solver import Solver
from solve.plotter import Plotter
from solve.tuner import Tuners, Tuner

game = CIA()
framework.load_game_data(game)
framework.new_game()
game.printWhenStreaming = False

# CIA_WALK.ADL is a log of an entire game walkthrough.
# Trim reduces the size of the game to the items seen in the specified number of steps
# Set steps to None to use the entire game
game.Trim(open(r"..\basic\CIA_WALK.ADL", "r"), steps=25)
framework.new_game()

solverData = SolverData()
solverData['ALPHA'] = 0.5
solverData['GAMMA'] = 0.65
solverData['TRAINING_EP'] = 0.5
solverData['TRAINING_EP_MIN'] = 0.1
solverData['TRAINING_EP_MAX'] = 1
solverData['TESTING_EP'] = 0.025
solverData['NUM_EPIS_TRAIN'] = 25
solverData['NUM_EPIS_TEST'] = 1
solverData['NUM_EPOCHS'] = 10000
solverData['MAX_STEPS'] = 40
solverData['PRINT_LOG_THRESHOLD'] = 100000
solverData['HIDDEN_SIZE'] = 500
solverData['ALREADY_SEEN_PENALTY'] = (-0.5, "subtract from reward when the state repeats")
solverData['NUM_RUNS'] = 1

strategy = CIAStrategy(game)

tune = False
if tune:
    tuners = Tuners([
        Tuner('ALPHA', 0.1, 0.7, 0.2),
        Tuner('GAMMA', 0.4, 0.7, 0.1),
        Tuner('TRAINING_EP', 0.45, 0.75, 0.1),
        # Tuner('TESTING_EP', 0.02, 0.06, 0.02),
        Tuner('HIDDEN_SIZE', 500, 2000, 500)
    ])

    solverData['NUM_EPIS_TRAIN'] = 30
    solverData['NUM_EPOCHS'] = 4
    solverData['MAX_STEPS'] = 18
    solverData['NUM_EPIS_TEST'] = 2
    solverData['NUM_TRIES'] = 6

    values, score, records = tuners.tune(solverData, lambda: Solver(framework, ModelPerVerbPredictor(strategy, hidden_size=solverData['HIDDEN_SIZE']), solverData, strategy))

    print("Tuned score, values:", score, values)

    print('\n'.join(map(lambda x: str(x), records)))
    records.sort(key=lambda x: x[0])
    print("*****sorted****")
    print('\n'.join(map(lambda x: str(x), records)))

    tuners.update_to_values(values)
else:
    # Tuned values
    solverData['ALPHA'] = 0.7
    solverData['GAMMA'] = 0.7
    solverData['TRAINING_EP'] = 0.65
    solverData['HIDDEN_SIZE'] = 1500

solverData['HIDDEN_SIZE'] = 1500
solverData['NUM_EPIS_TRAIN'] = 30
solverData['NUM_EPOCHS'] = 10000
solverData['MAX_STEPS'] = 40

#solver = Solver(framework, ModelPerActionPredictor(DQN), solverData, strategy)
#solver = Solver(framework, ModelPerVerbPredictor(DQN), solverData, strategy)
#solver = Solver(framework, ModelPerObjectPredictor(DQN), solverData, strategy)
solver = Solver(framework, DecoupledPredictor(DQN), solverData, strategy)

Plotter(solver.execute(), solverData)

