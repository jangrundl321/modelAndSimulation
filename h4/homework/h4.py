import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from tabulate import tabulate


# ## 4.2.1

def Simulation(forest,fire,k_1,k_3):
    forestFire = (forest,fire)
    x = []
    x.append((forest,fire))
    k_2 = 0.1
    t = 0
    time = 0
    max_fire = 0
    forest_list = []
    fire_list = []
    while t <= 1 and fire >0:
        more_forest = k_1*forest
        more_fire_less_forest = k_2*forest*fire
        less_fire = k_3*fire
        total = more_forest + more_fire_less_forest + less_fire
        total_rand = random.randint(0,int(total))
        rand = random.uniform(0,1)
        if rand == 1:
            continue
        next_step = np.log(1-rand)/(-total)
        if total_rand <= more_forest:
            forest += 1
            x.append((forest,fire))
        elif more_forest < total_rand <= more_forest + more_fire_less_forest:
            forest -= 1
            fire += 1
            x.append((forest,fire))
        else:
            fire -= 1
            x.append((forest,fire))
        if fire > max_fire:
            max_fire = fire
            time = t
        else:
            pass
        t += np.log(1-rand)/(-total)
        forest_list.append(forest)
        fire_list.append(fire)
    return time,max_fire



parameter_arr = np.zeros((10,10))
for k_1 in range(1,11):
    for k_3 in range(1,11):
        result = Simulation(100,3,k_1,k_3)
        time = result[0]
        max_fire = result[1]
        x = math.sqrt((abs(1 - (max_fire / 500))) ** 2 + (abs(1 - (time / 0.3))) ** 2)
        parameter_arr[(k_1-1,k_3-1)] = x

data = parameter_arr.transpose()
colorCoding = cm.get_cmap('viridis', 100)
n = len([colorCoding])
fig, axs = plt.subplots(1, n, figsize=(10, 10),constrained_layout=True, squeeze=False)
for [ax, cmap] in zip(axs.flat, [colorCoding]):
    psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=0, vmax=1.6)
    fig.colorbar(psm, ax=ax)
ax.set_ylabel('k3')
ax.set_xlabel('k1')
plt.show()


# ## 4.2.2

def HillClimbing(x,y,optimizationSteps):
    value = parameter_arr[(x,y)]
    while value > 0.15:
        optimizationSteps += 1
        if x==90 or y==90:
            HillClimbing(random.randint(0,90),random.randint(0,90),optimizationSteps)
        else:
            value_1 = round(parameter_arr[(x,y)],5)
            value_2 = round(parameter_arr[(x+1,y)],5)
            value_3 = round(parameter_arr[(x-1,y)],5)
            value_4 = round(parameter_arr[(x,y+1)],5)
            value_5 = round(parameter_arr[(x,y-1)],5)
            value = min(value_1,value_2,value_3,value_4,value_5)
                
            eif value == value_1:
                x = random.randint(0,90)
                y = random.randint(0,90)
                HillClimbing(x,y,optimizationSteps)
            elif value == value_2:
                x += 1
                HillClimbing(x,y,optimizationSteps)
            elif value == value_3:
                x -= 1
                HillClimbing(x,y,optimizationSteps)
            elif value == value_4:
                y += 1
                HillClimbing(x,y,optimizationSteps)
            elif value == value_5:
                y -= 1
                HillClimbing(x,y,optimizationSteps)
            
    k_1 = 1 + x/10
    k_3 = 1 + x/10
    return(value,k_1,k_3,optimizationSteps)
            



optimizationSteps_total = 0
for i in range(1,11):
    parameter_arr = np.zeros((91,91))
    x = -1
    for k_1 in np.arange(1,10.1,0.1):
        x +=1
        y = -1
        for k_3 in np.arange(1,10.1,0.1):
            y += 1
            result = Simulation(100,3,round(k_1,1),round(k_3,1))
            time = result[0]
            max_fire = result[1]
            value = math.sqrt((abs(1 - (max_fire / 500))) ** 2 + (abs(1 - (time / 0.3))) ** 2)
            parameter_arr[(x,y)] = value
    x = random.randint(0,90) 
    y = random.randint(0,90)
    optimizationSteps = 0
    value = HillClimbing(x,y,optimizationSteps)
    optimizationSteps_total += value[3]
print("Durschnitt: ",optimizationSteps_total/10)
