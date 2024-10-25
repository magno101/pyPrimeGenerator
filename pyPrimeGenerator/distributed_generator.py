import logging
from sympy import isprime, primerange, fibonacci
from concurrent.futures import ProcessPoolExecutor, as_completed

# Setup logging
logging.basicConfig(filename="extended_mersenne_primes.log", level=logging.INFO, format="%(message)s")

# Generate prime constants for C up to a specified limit
def generate_constants(limit):
    """Generates a list of primes up to a given limit for C values."""
    return list(primerange(41, limit))

# Prime sequence filters
def prime_fibonacci_sequence(n):
    """Generates prime Fibonacci numbers up to the nth Fibonacci."""
    primes = []
    for i in range(n + 1):
        fib = fibonacci(i)
        if isprime(fib):
            primes.append(fib)
    return primes

def lucas_sequence_primes(n):
    """Generates prime Lucas numbers up to the nth Lucas number."""
    lucas_primes = []
    a, b = 2, 1
    for i in range(n + 1):
        if isprime(a):
            lucas_primes.append(a)
        a, b = b, a + b
    return lucas_primes

def pell_sequence_primes(n):
    """Generates prime Pell numbers up to the nth Pell number."""
    pell_primes = []
    a, b = 0, 1
    for i in range(n + 1):
        if isprime(a):
            pell_primes.append(a)
        a, b = b, 2 * a + b
    return pell_primes

# Quadratic formula calculation
def quadratic_formula(n, C):
    """Applies the quadratic formula f(n) = n^2 + n + C."""
    return n**2 + n + C

# Test values of f(n) for each constant C and filtered indices
def test_quadratic_with_filter(constants, prime_indices):
    results = {}
    for C in constants:
        results[C] = []  # Stores (n, f(n), is_prime) for each prime index
        for n in prime_indices:
            value = quadratic_formula(n, C)
            if isprime(value):
                results[C].append((n, value, True))
            else:
                results[C].append((n, value, False))
    return results

# Optimized Mersenne prime test for very large p values
def is_large_mersenne_prime(p):
    """Efficiently checks if 2^p - 1 is a Mersenne prime for high p values."""
    mersenne_candidate = (2 ** p) - 1
    if isprime(mersenne_candidate):
        logging.info(f"Mersenne prime found: 2^{p} - 1")
        return p, mersenne_candidate
    return None

def generate_primes_distributed(c_limit=20000, sequence_limit=200, mersenne_limit=100000):
    """Generates primes using the specified parameters with distributed processing."""
    # Generate constants and sequence filters based on input parameters
    expanded_constants = generate_constants(c_limit)
    fibonacci_primes_extended = prime_fibonacci_sequence(sequence_limit)
    lucas_primes_extended = lucas_sequence_primes(sequence_limit)
    pell_primes_extended = pell_sequence_primes(sequence_limit)

    # Combine the extended sequence filters
    combined_prime_indices_extended = sorted(set(fibonacci_primes_extended + lucas_primes_extended + pell_primes_extended))

    # Run the quadratic formula test with combined sequence filters
    scaled_results_extended = test_quadratic_with_filter(expanded_constants, combined_prime_indices_extended)

    # Extract prime values from results for Mersenne testing, prioritizing larger p values for testing
    scaled_mersenne_candidates_extended = sorted({result for C, values in scaled_results_extended.items() for n, result, is_prime in values if is_prime})

    # Run Mersenne testing in parallel on filtered candidates up to mersenne_limit
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(is_large_mersenne_prime, p): p for p in scaled_mersenne_candidates_extended if p < mersenne_limit}
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(f"Found large Mersenne prime: 2^{result[0]} - 1")

# Define main function for command-line execution
def main():
    import argparse
    # Argument parser for adjustable parameters
    parser = argparse.ArgumentParser(description="Distributed Prime Generator with Adjustable Parameters.")
    parser.add_argument("--c_limit", type=int, default=20000, help="Upper limit for prime constants C (default: 20000)")
    parser.add_argument("--sequence_limit", type=int, default=200, help="Number of terms for Fibonacci, Lucas, and Pell sequences (default: 200)")
    parser.add_argument("--mersenne_limit", type=int, default=100000, help="Upper limit for Mersenne test values of p (default: 100000)")
    args = parser.parse_args()
    
    # Call generate_primes_distributed with parsed arguments
    generate_primes_distributed(c_limit=args.c_limit, sequence_limit=args.sequence_limit, mersenne_limit=args.mersenne_limit)
