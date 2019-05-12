"""
Section 3.1 The Number Partitioning Problem
Partition a set of numbers into two subsets such that the subset sums are as close to each other as possible.

Test list size 100 - too big to solve on the D-Wave 2000Q, so we have to use
a decomposer to break the large problem into sub-problems.
"""

import copy
import dimod
import hybrid
import random
import sys
import time
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

def generate_numbers(num_numbers):
    random.seed(51229)
    numbers = random.sample(xrange(1, 1000), num_numbers)
    return numbers

def to_bqm(numbers):
    c = sum(numbers)
    c_square = c**c

    linear = {}
    quadratic = {}
    offset = 0.0
    vartype = dimod.BINARY
    for index, value in enumerate(numbers):
        linear[index+1] = value * (value - c)
    for index1, value1 in enumerate(numbers[:-1]):
        for index2 in range(index1+1, len(numbers)):
            value = value1 * numbers[index2]
            idx = (index1+1, index2+1)
            quadratic[idx] = quadratic[tuple(reversed(idx))] = value

    bqm = dimod.BinaryQuadraticModel(
        linear, 
        quadratic, 
        offset, 
        vartype)
    print len(linear)
    print len(quadratic)
    return bqm

def solve(sampler, bqm, num_reads=None):
    params = {}
    if num_reads:
        params['num_reads'] = num_reads
    return sampler.sample(bqm, **params)

def split_numbers_list(numbers, result):
    list1 = []
    list2 = []
    for key, include_in_list in result.items():
        index = key-1
        if include_in_list:
            list1.append(numbers[index])
        else:
            list2.append(numbers[index])
    return list1, list2

def print_result(sample_set):
    for sample in sample_set.samples():
        list1, list2 = split_numbers_list(numbers, sample)
        print "list1: {}, sum: {}, list2: {}, sum: {}".format(list1, sum(list1), list2, sum(list2))

dwave_sampler = EmbeddingComposite(DWaveSampler())

print "#"*80
numbers = generate_numbers(100)  # generate a list of numbers to be split into equal sums
bqm = to_bqm(numbers)

# Redefine the workflow: a rolling decomposition window
subproblem = hybrid.EnergyImpactDecomposer(size=50, rolling_history=0.15)
subsampler = hybrid.QPUSubproblemAutoEmbeddingSampler() | hybrid.SplatComposer()

iteration = hybrid.RacingBranches(
    subproblem | subsampler
) | hybrid.ArgMin()

subsampler = hybrid.Map(
    hybrid.QPUSubproblemAutoEmbeddingSampler()
) | hybrid.Reduce(
    hybrid.Lambda(merge_substates)
) | hybrid.SplatComposer()


workflow = hybrid.LoopUntilNoImprovement(iteration, convergence=3)

init_state = hybrid.State.from_problem(bqm)

start = time.time()
final_state = workflow.run(init_state).result()
end = time.time()
print "Using dwave-hybrid (elapsed time: {}s)".format(end-start)
print(final_state.samples)
print_result(final_state.samples)
print ""

# Using dwave-hybrid (elapsed time: 17.1963908672s)
#    1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 ... 100       energy num_oc.
# 0  0  1  1  0  0  0  1  1  1  1  0  0  1  1  1  0 ...   1 -460370757.0       1
# ['BINARY', 1 rows, 1 samples, 100 variables]
# list1: [447, 112, 485, 293, 452, 173, 106, 66, 320, 235, 259, 87, 204, 336, 165, 248, 104, 98, 68, 471, 255, 269, 466, 23, 82, 397, 254, 6, 196, 241, 423, 402, 80, 309, 152, 435, 478, 231, 130, 377, 477, 407, 261, 39, 418, 17, 111, 333, 464, 1], sum: 12463, list2: [871, 488, 831, 605, 902, 966, 579, 983, 750, 883, 958, 744, 591, 486, 507, 988, 959, 496, 648, 669, 541, 537, 504, 956, 944, 569, 864, 985, 521, 601, 916, 581, 715, 926, 889, 820, 787, 526, 666, 987, 533, 499, 665, 742, 913, 679, 868, 845, 783, 673], sum: 36939

# TODO: Optimize the solution