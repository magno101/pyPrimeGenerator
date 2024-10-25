# pyPrimeGenerator

`pyPrimeGenerator` is a Python package for generating large prime numbers using a combination of the quadratic formula, sequence-based filters (Fibonacci, Lucas, and Pell), and Mersenne prime testing. The package includes both local and distributed modes for flexible computation, depending on the workload and system capabilities.

## Features

- **Quadratic Formula Primes**: Uses quadratic sequences to generate potential primes.
- **Sequence Filters**: Employs Fibonacci, Lucas, and Pell sequence-based filters to refine results.
- **Mersenne Prime Testing**: Optionally performs Mersenne prime tests, suitable for both smaller and larger values of \( p \).
- **Distributed Mode**: Parallel processing capabilities for high-performance systems.

## Requirements

- Python 3.x
- Required library: `sympy`

Install dependencies with:
```bash
pip install sympy
```

## Installation
```bash
git clone https://github.com/magno101/pyPrimeGenerator.git
cd pyPrimeGenerator
pip install .
```

## Usage
### Local Mode
```bash
primegen-local --c_limit 10000 --sequence_limit 100 --mersenne_limit 50000
```

### Distributed Mode
```bash
primegen-distributed --c_limit 20000 --sequence_limit 200 --mersenne_limit 100000
```
