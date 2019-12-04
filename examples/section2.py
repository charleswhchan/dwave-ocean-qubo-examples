"""
Section 2: Illustrative Examples and Definitions
"""

import dimod
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

linear = {1: -5, 2: -3, 3: -8, 4: -6}
quadratic = {(1, 2): 4, (1, 3): 8, (2, 3): 2, (3, 4): 10}
offset = 0.0
vartype = dimod.BINARY

# Expected Solution
#
#   y = -11
#   x1 = 1
#   x2 = 0
#   x3 = 0
#   x4 = 1

bqm = dimod.BinaryQuadraticModel(linear, quadratic, offset, vartype)
sampler = dimod.ExactSolver()
sample_set = sampler.sample(bqm)
print("Using ExactSolver()")
print(sample_set)

# Using ExactSolver()
#     1  2  3  4 energy num_oc.
# 14  1  0  0  1  -11.0       1
# 13  1  1  0  1  -10.0       1
# 4   0  1  1  0   -9.0       1
# 12  0  1  0  1   -9.0       1
# 7   0  0  1  0   -8.0       1
# 15  0  0  0  1   -6.0       1
# 1   1  0  0  0   -5.0       1
# 6   1  0  1  0   -5.0       1
# 11  0  1  1  1   -5.0       1
# 2   1  1  0  0   -4.0       1
# 8   0  0  1  1   -4.0       1
# 3   0  1  0  0   -3.0       1
# 5   1  1  1  0   -2.0       1
# 9   1  0  1  1   -1.0       1
# 0   0  0  0  0    0.0       1
# 10  1  1  1  1    2.0       1
# ['BINARY', 16 rows, 16 samples, 4 variables]

print("#" * 80)

sampler = dimod.SimulatedAnnealingSampler()
sample_set = sampler.sample(bqm)
print("Using SimulatedAnnlearingSampler()")
print(sample_set)

# Using SimulatedAnnlearingSampler()
#    1  2  3  4 energy num_oc.
# 0  1  0  0  1  -11.0       1
# 1  1  0  0  1  -11.0       1
# 2  1  0  0  1  -11.0       1
# 3  1  0  0  1  -11.0       1
# 4  1  0  0  1  -11.0       1
# 5  1  0  0  1  -11.0       1
# 6  1  0  0  1  -11.0       1
# 7  1  0  0  1  -11.0       1
# 8  1  0  0  1  -11.0       1
# 9  1  0  0  1  -11.0       1
# ['BINARY', 10 rows, 10 samples, 4 variables]

print("#" * 80)

# Pre-requisite: Make sure your environment is setup using
#   dwave config create
# See: https://docs.ocean.dwavesys.com/en/latest/overview/dwavesys.html#configuring-a-d-wave-system-as-a-solver
#
# For more information about the DWaveSampler(), refer to https://dwave-systemdocs.readthedocs.io/en/latest/reference/samplers/dwave_sampler.html#module-dwave.system.samplers.dwave_sampler
sampler = EmbeddingComposite(DWaveSampler())
sample_set = sampler.sample(bqm)
print("Using DWaveSampler()")
print(sample_set)

# Using DWaveSampler()
#    1  2  3  4 energy num_oc. chain_.
# 0  1  0  0  1  -11.0       1     0.0
# ['BINARY', 1 rows, 1 samples, 4 variables]
