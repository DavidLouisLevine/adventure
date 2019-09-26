import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    def __init__(self, epoch_rewards_test, solverData):
        epoch_rewards_test = np.array(epoch_rewards_test)

        x = np.arange(solverData['NUM_EPOCHS'])
        fig, axis = plt.subplots()
        axis.plot(x, np.mean(epoch_rewards_test,
                             axis=0))  # plot reward per epoch averaged per run
        axis.set_xlabel('Epochs')
        axis.set_ylabel('reward')
        axis.set_title(('Linear: nRuns=%d, Epilon=%.2f, Epi=%d, alpha=%.4f' %
                        (solverData['NUM_RUNS'], solverData['TRAINING_EP'], solverData['NUM_EPIS_TRAIN'],
                         solverData['ALPHA'])))
        plt.show()
