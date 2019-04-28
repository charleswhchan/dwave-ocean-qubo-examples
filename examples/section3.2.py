"""
Section 3.2 The Max Cut Problem
Given an undirected graph G(V,E) with a vertex set V and an edge set E, the Max Cut problem seeks to partition V into two sets such that the number of edges between the two sets (considered to be severed by the cut), is a large as possible.
"""

import dimod
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

linear = {1: -2, 2: -2, 3: -3, 4: -3, 5: -2}
quadratic = {(1, 2): 1, 
             (1, 3): 1, 
             (2, 1): 1,
             (2, 4): 1,
             (3, 1): 1,
             (3, 4): 1,
             (3, 5): 1,
             (4, 2): 1,
             (4, 5): 1,
             (5, 3): 1,
             (5, 4): 1}
offset = 0.0
vartype = dimod.BINARY

# Expected Solution
#
#   x = (0, 1, 1, 0, 0)
#   Hence vertices 2 and 3 are in one set and vertices 1, 4, and 5 are in the other, with a maximum cut value of 5

bqm = dimod.BinaryQuadraticModel(
    linear, 
    quadratic, 
    offset, 
    vartype)
sampler = dimod.ExactSolver()
sample_set = sampler.sample(bqm)
print "Using ExactSolver()"
print sample_set

# Using ExactSolver()
#     1  2  3  4  5 energy num_oc.
# 4   0  1  1  0  0   -5.0       1
# 8   0  0  1  1  0   -5.0       1
# 9   1  0  1  1  0   -5.0       1
# 11  0  1  1  1  0   -5.0       1
# 14  1  0  0  1  0   -5.0       1
# ...
# 0   0  0  0  0  0    0.0       1
# ['BINARY', 32 rows, 32 samples, 5 variables]

print '#'*80

sampler = dimod.SimulatedAnnealingSampler()
sample_set = sampler.sample(bqm)
print "Using SimulatedAnnlearingSampler()"
print sample_set

# Using SimulatedAnnlearingSampler()
#    1  2  3  4  5 energy num_oc.
# 0  1  0  1  1  0   -5.0       1
# 1  1  0  0  1  0   -5.0       1
# 2  0  0  1  1  0   -5.0       1
# 3  1  0  0  1  1   -5.0       1
# 4  0  1  1  1  0   -5.0       1
# 5  1  0  0  1  1   -5.0       1
# 6  1  0  1  1  0   -5.0       1
# 7  0  1  1  0  1   -5.0       1
# 8  1  0  0  1  1   -5.0       1
# 9  1  0  0  1  1   -5.0       1
# ['BINARY', 10 rows, 10 samples, 5 variables]

print '#'*80

sampler = EmbeddingComposite(DWaveSampler())
sample_set = sampler.sample(bqm, num_reads=50)
print "Using DWaveSampler()"
print sample_set

# Using DWaveSampler()
#    1  2  3  4  5 energy num_oc. chain_.
# 0  0  1  1  0  0   -5.0       8     0.0
# 1  1  0  1  1  0   -5.0       2     0.0
# 2  0  1  1  0  1   -5.0      11     0.0
# 3  1  0  0  1  1   -5.0      13     0.0
# 4  0  0  1  1  0   -5.0       4     0.0
# 5  0  1  1  1  0   -5.0       9     0.0
# 6  1  0  0  1  0   -5.0       3     0.0
# ['BINARY', 7 rows, 50 samples, 5 variables]