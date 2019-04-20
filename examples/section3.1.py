"""
Section 3.1 The Number Partitioning Problem
Partition a set of numbers into two subsets such that the subset sums are as close to each other as possible.
"""

import copy
import dimod
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

numbers = [25,7,13,31,42,17,21,10]
print numbers

print "#"*80

# First try to solve using classical computing / programming naively.
# Sort the list in ascending order and then split it into 2 list based on odd and even index position
numbers_copy = copy.deepcopy(numbers)
numbers_copy.sort()
list1 = numbers_copy[0::2]
list2 = numbers_copy[1::2]
print "Using classical computing / programming"
print "list1: {}, sum: {}".format(list1, sum(list1))
print "list2: {}, sum: {}".format(list2, sum(list2))
print "diff: abs(sum(list1) - sum(list2)) = {}".format(abs(sum(list1) - sum(list2)))

# Using classical computing / programming
# list1: [7, 13, 21, 31], sum: 72
# list2: [10, 17, 25, 42], sum: 94
# diff: abs(sum(list1) - sum(list2)) = 22

print "#"*80

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
# print linear
# print quadratic

# Expected Solution
# x=(0,0,0,1,1,0,0,1), ie list1=[31,42,10]; list2=[25,7,13,17,21]
# y=-6889

bqm = dimod.BinaryQuadraticModel(
    linear, 
    quadratic, 
    offset, 
    vartype)
sampler = dimod.ExactSolver()
sample_set = sampler.sample(bqm)
sample_set = sample_set.truncate(5)
print "Using ExactSolver()"
print sample_set
for sample in sample_set.samples():
    list1, list2 = split_numbers_list(numbers, sample)
    print "list1: {}, sum: {}, list2: {}, sum: {}".format(list1, sum(list1), list2, sum(list2))

# Print the first 5 results, notice there are multiple solutions that achieve 
# the right answer.
#
# Using ExactSolver()
#    1  2  3  4  5  6  7  8  energy num_oc.
# 0  0  0  0  1  1  0  0  1 -6889.0       1
# 1  0  1  1  0  1  0  1  0 -6889.0       1
# 2  1  1  1  0  0  1  1  0 -6889.0       1
# 3  1  0  0  1  0  1  0  1 -6889.0       1
# 4  1  1  0  1  0  0  1  0 -6888.0       1
# ['BINARY', 5 rows, 5 samples, 8 variables]
# list1: [31, 42, 10], sum: 83, list2: [25, 7, 13, 17, 21], sum: 83
# list1: [7, 13, 42, 21], sum: 83, list2: [25, 31, 17, 10], sum: 83
# list1: [25, 7, 13, 17, 21], sum: 83, list2: [31, 42, 10], sum: 83
# list1: [25, 31, 17, 10], sum: 83, list2: [7, 13, 42, 21], sum: 83
# list1: [25, 7, 31, 21], sum: 84, list2: [13, 42, 17, 10], sum: 82

print '#'*80

sampler = dimod.SimulatedAnnealingSampler()
sample_set = sampler.sample(bqm)
sample_set = sample_set.truncate(5)
print "Using SimulatedAnnlearingSampler()"
print sample_set
for sample in sample_set.samples():
    list1, list2 = split_numbers_list(numbers, sample)
    print "list1: {}, sum: {}, list2: {}, sum: {}".format(list1, sum(list1), list2, sum(list2))

# Using SimulatedAnnlearingSampler()
#    1  2  3  4  5  6  7  8  energy num_oc.
# 0  0  0  0  1  1  0  0  1 -6889.0       1
# 1  1  1  1  0  0  1  1  0 -6889.0       1
# 2  1  1  0  0  1  0  0  1 -6888.0       1
# 3  0  0  0  0  1  1  1  0 -6880.0       1
# 4  0  0  0  0  1  1  1  0 -6880.0       1
# ['BINARY', 5 rows, 5 samples, 8 variables]
# list1: [31, 42, 10], sum: 83, list2: [25, 7, 13, 17, 21], sum: 83
# list1: [25, 7, 13, 17, 21], sum: 83, list2: [31, 42, 10], sum: 83
# list1: [25, 7, 42, 10], sum: 84, list2: [13, 31, 17, 21], sum: 82
# list1: [42, 17, 21], sum: 80, list2: [25, 7, 13, 31, 10], sum: 86
# list1: [42, 17, 21], sum: 80, list2: [25, 7, 13, 31, 10], sum: 86

print '#'*80

sampler = EmbeddingComposite(DWaveSampler())
esponse = sampler.sample(bqm)
sample_set = sample_set.truncate(5)
print "Using DWaveSampler()"
print sample_set
for sample in sample_set.samples():
    list1, list2 = split_numbers_list(numbers, sample)
    print "list1: {}, sum: {}, list2: {}, sum: {}".format(list1, sum(list1), list2, sum(list2))

# Using DWaveSampler()
#    1  2  3  4  5  6  7  8  energy num_oc.
# 0  0  0  0  1  1  0  0  1 -6889.0       1
# 1  1  1  0  1  0  0  1  0 -6888.0       1
# 2  1  1  1  1  0  0  0  1 -6880.0       1
# 3  0  0  0  0  1  1  1  0 -6880.0       1
# 4  1  0  1  0  1  0  0  0 -6880.0       1
# ['BINARY', 5 rows, 5 samples, 8 variables]
# list1: [31, 42, 10], sum: 83, list2: [25, 7, 13, 17, 21], sum: 83
# list1: [25, 7, 31, 21], sum: 84, list2: [13, 42, 17, 10], sum: 82
# list1: [25, 7, 13, 31, 10], sum: 86, list2: [42, 17, 21], sum: 80
# list1: [42, 17, 21], sum: 80, list2: [25, 7, 13, 31, 10], sum: 86
# list1: [25, 13, 42], sum: 80, list2: [7, 31, 17, 21, 10], sum: 86