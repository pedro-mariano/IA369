#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import array
import random
import json
import numpy
import time

from math import sqrt

from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

toolbox = base.Toolbox()

def uniform(low, up, size=None):
    try:
        return [random.uniform(a, b) for a, b in zip(low, up)]
    except TypeError:
        return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]

def main(function,NGEN,MU,refPoint):

    # Problem definition
    # Functions zdt1, zdt2, zdt3, zdt6 have bounds [0, 1]
    # Functions zdt4 has bounds x1 = [0, 1], xn = [-5, 5], with n = 2, ..., 10
    # Functions zdt1, zdt2, zdt3 have 30 dimensions, zdt4 and zdt6 have 10
    if(function == 'ZDT4'):
        NDIM = 10
        BOUND_LOW, BOUND_UP = [0.0] + [-5.0]*(NDIM-1), [1.0] + [5.0]*(NDIM-1)
    else:
        NDIM = 30
        if(function == 'ZDT6'):
            NDIM = 10
        BOUND_LOW, BOUND_UP = [0.0]*NDIM, [1.0]*NDIM

##    print 'refPoint =' ,refPoint
##    print 'NDIM=',NDIM
##    print 'BOUNDS=',BOUND_LOW,BOUND_UP
##    print 'NGEN=', NGEN
##    print 'MU=',MU

    toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", eval(''.join(['benchmarks.zdt',function[3]])))
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=30.0)
    toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM)
    toolbox.register("select", tools.selNSGA2)

    CXPB = 1.0

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    # stats.register("avg", numpy.mean, axis=0)
    # stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    hvValues = []
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
    pop = toolbox.population(n=MU)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    hvValues.append(hypervolume(pop, refPoint))

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))
    
    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    #print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]
        
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
            
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        #print(logbook.stream)

        hvValues.append(hypervolume(pop, refPoint))

    print 'Hypervolume = ', hvValues[-1]

    return pop, logbook, hvValues
        
def runNSGA2(seed,function,nReps,NEval,NPop,refPoint):

    print 'Running NSGA-II\n'

    with open(''.join(['../dev/pareto_front/zdt',function[3],'_front.json'])) as optimal_front_data:
        optimal_front = json.load(optimal_front_data)
    # Use 500 of the 1000 points in the json file
    # optimal_front = sorted(optimal_front[i] for i in range(0, len(optimal_front), 2))

    hvValues = []
    conv = []
    diver = []
    fronts = []

    NGEN = NEval/NPop

    random.seed(seed)
   
    for nexec in xrange(nReps):

        print 'Starting execution %d ...' % (nexec+1)

        start = time.time()
    
        pop, stats, hv = main(function,NGEN,NPop,refPoint)
        hvValues.append(hv)
        #pop.sort(key=lambda x: x.fitness.values)

        # print(stats)
        conv.append(convergence(pop, optimal_front))
        #diver.append(diversity(pop, optimal_front[0], optimal_front[-1]))
        print 'Convergence metric = ', conv[nexec]
        #print("Diversity: ", diver[nexec])
               
        front = numpy.array([ind.fitness.values for ind in pop])
        fronts.append(front.tolist())
        #optimal_front = numpy.array(optimal_front)
        #plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
        #plt.scatter(front[:,0], front[:,1], c="b")
        #plt.axis("tight")

        end = time.time()
        print 'Execution %d  completed in  %f seconds\n' % (nexec+1,end-start)

##        if(nReps == 1):
##            plt.show()
##        else:
##            plt.savefig(''.join(['results/figures/NSGA2_',function,'_exec',str(nexec),'.png']), bbox_inches='tight')

    finalHV = [x[-1] for x in hvValues]
    print 'Average hypervolume=', sum(finalHV)/nReps
    print 'Best hypervolume=', max(finalHV)

    with open(''.join(['../dev/files/Pop_',function,'_NSGA2.json']),'w') as outfile:
        json.dump(fronts,outfile)

    with open(''.join(['../dev/files/HV_',function,'_NSGA2.json']),'w') as outfile:
        json.dump(hvValues,outfile)

    with open(''.join(['../dev/files/conv_',function,'_NSGA2.json']),'w') as outfile:
        json.dump(conv,outfile)

##    with open(''.join(['../dev/files/diver_',function,'_NSGA2.json']),'w') as outfile:
##        json.dump(diver,outfile)

    print '\nNSGA-II finished all experiments\n'

