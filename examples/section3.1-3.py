"""
Section 3.1 The Number Partitioning Problem
Partition a set of numbers into two subsets such that the subset sums are as close to each other as possible.

Test list size 100 - too big to solve on the D-Wave 2000Q using minor-embedding, 
so we have to use a decomposer to break the large problem into sub-problems.
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
    numbers = random.sample(xrange(1, 2000), num_numbers)
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

def print_result(sample_set, sum_only=True):
    for sample in sample_set.samples():
        list1, list2 = split_numbers_list(numbers, sample)
        if sum_only:
            print "sum1: {}, sum2: {}".format(sum(list1), sum(list2))
        else:
            print "list1: {}, sum1: {}, list2: {}, sum2: {}".format(list1, sum(list1), list2, sum(list2))

dwave_sampler = EmbeddingComposite(DWaveSampler())

print "#"*80
numbers = generate_numbers(1000)  # generate a list of numbers to be split into equal sums
bqm = to_bqm(numbers)

# Change rolling_history=0.5, traversal='bfs' and num_reads=1000
decomposer = hybrid.EnergyImpactDecomposer(size=50, rolling_history=0.5, traversal='bfs')
sampler = hybrid.QPUSubproblemAutoEmbeddingSampler(num_reads=1000) 
composer = hybrid.SplatComposer()

iteration = hybrid.RacingBranches(decomposer | sampler | composer) | hybrid.ArgMin()

workflow = hybrid.LoopUntilNoImprovement(iteration, convergence=3)

init_state = hybrid.State.from_problem(bqm)

start = time.time()
final_state = workflow.run(init_state).result()
end = time.time()
print "Using dwave-hybrid (elapsed time: {}s)".format(end-start)
print(final_state.samples)
print_result(final_state.samples)
print ""

# Using dwave-hybrid (elapsed time: 415.669251919s)
#    1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 ... 1000          energy num_oc.
# 0  1  1  1  1  1  1  1  1  1  1  1  1  0  1  1 ...    0 -250256565786.0       1
# ['BINARY', 1 rows, 1 samples, 1000 variables]
# sum1: 500254, sum2: 500259