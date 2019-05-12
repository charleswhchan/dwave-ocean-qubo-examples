# dwave-qubo-ocean-examples
Implement examples from [A Tutorial on Formulating and Using QUBO Models](https://arxiv.org/pdf/1811.11538.pdf) using [D-Wave Ocean SDK](https://github.com/dwavesystems/dwave-ocean-sdk)

- [Section 2: Illustrative Examples and Definitions](examples/section2.py)
- Section 3: Natural QUBO Formulations
  - [Section 3.1: The Number Partitioning Problem](examples/section3.1.py)
    - [List size 50](examples/section3.1-1.py) (using minor-embedding on D-Wave 2000Q)
    - [List size 100](examples/section3.1-2.py) (using dwave-hybrid to decomposite the problem)
  - [Section 3.2: The Max Cut Problem](examples/section3.2.py)
- Section 4: Creating QUBO Models Using Known Penalties
- Section 5: Creating QUBO Models Using a General Purpose Approach

References:
- [D-Wave Problem-Solving Handbook](https://docs.dwavesys.com/docs/latest/doc_handbook.html)
- [D-Wave Ocean Software Documentation](https://docs.ocean.dwavesys.com/en/latest/index.html)
  - [Tools](https://docs.ocean.dwavesys.com/en/latest/projects.html)
