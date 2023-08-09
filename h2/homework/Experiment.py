# implementation of exercise 2.2.3
# Experiment.py contains the file to run the DEVS experiment based on Simulator.py and Modell.py
# comment/TODO:
# - Because of some mistakes in the Simulator.py Classes. It doesnt return the needed results.


from Simulator import Simulator as sim
from Simulator import Coordinator as coordinator
from Simulator import RootCoordinator as rootCoordinator
from Simulator import devs_simulator as devs_simulator
from Modell import RootModel as rootModel
import matplotlib.pyplot as plt
import random as random

# setting random seed to 0
random.seed(0)
# defining 'constant' parameters
row, col = 21, 21
number_of_repetitions = 100
simulation_steps = 1000

#################################################################################################################
# initiate and specify the process structure for the DEVS experiment

RootModel = rootModel(row, col)

children_of_root_model = [RootModel.match]
for r in range(row):
    for c in range(col):
        children_of_root_model.append(RootModel.root_model_grid[r][c])

simulators = []
for child in children_of_root_model:
    simulators.append(sim(child))

RootCoordinator = rootCoordinator()
RootModelCoordinator = coordinator(RootCoordinator, simulators, RootModel)
RootCoordinator.child = RootModelCoordinator
for simulator in simulators:
    simulator.parent = RootModelCoordinator

######################################################################################################################
# the actual experiment implementation

histogram_of_sum_of_burning_regions = [0] * simulation_steps

for i in range(number_of_repetitions):
    n = 0
    for s in range(simulation_steps):
        status = devs_simulator(RootCoordinator)
        num_of_burning_regions = 0
        for x, y in status.items():
            if y == "fire" and x != "Match":
                num_of_burning_regions += 1
        histogram_of_sum_of_burning_regions[n] += num_of_burning_regions
        n += 1
    RootCoordinator.reset()

histogram_of_averages_of_burning_regions = [x / number_of_repetitions for x in histogram_of_sum_of_burning_regions]
Y = histogram_of_averages_of_burning_regions

print(histogram_of_sum_of_burning_regions)
print(Y)

###################################################################################################################
# plot graph

plt.plot(Y)
plt.xlabel('simulation time')
plt.ylabel('avg burning regions')
plt.show()







