import logging
from sympy import isprime, primerange, fibonacci

# Setup logging
logging.basicConfig(filename="local_mersenne_primes.log", level=logging.INFO, format="%(message)s")

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

# Mersenne prime test for local execution
def is_mersenne_prime(p):
    """Checks if 2^p - 1 is a Mersenne prime."""
    mersenne_candidate = (2 ** p) - 1
    if isprime(mersenne_candidate):
        logging.info(f"Mersenne prime found: 2^{p} - 1")
        return p, mersenne_candidate
    return None

def generate_primes(c_limit=10000, sequence_limit=100, mersenne_limit=50000):
    """Generates primes using the specified parameters for C limit, sequence limit, and Mersenne limit."""
    # Generate constants and sequence filters based on input parameters
    expanded_constants = generate_constants(c_limit)
    fibonacci_primes_extended = prime_fibonacci_sequence(sequence_limit)
    lucas_primes_extended = lucas_sequence_primes(sequence_limit)
    pell_primes_extended = pell_sequence_primes(sequence_limit)

    # Combine the extended sequence filters
    combined_prime_indices_extended = sorted(set(fibonacci_primes_extended + lucas_primes_extended + pell_primes_extended))

    # Run the quadratic formula test with combined sequence filters
    scaled_results_extended = test_quadratic_with_filter(expanded_constants, combined_prime_indices_extended)

    # Extract prime values from results for Mersenne testing, filtering up to specified p limit
    scaled_mersenne_candidates_extended = sorted({result for C, values in scaled_results_extended.items() for n, result, is_prime in values if is_prime})

    # Run Mersenne testing on filtered candidates
    for p in scaled_mersenne_candidates_extended:
        if p < mersenne_limit:
            result = is_mersenne_prime(p)
            if result:
                print(f"Found Mersenne prime: 2^{result[0]} - 1")

# Define main function for command-line execution
def main():
    import argparse
    # Argument parser for adjustable parameters
    parser = argparse.ArgumentParser(description="Local Prime Generator with Adjustable Parameters.")
    parser.add_argument("--c_limit", type=int, default=10000, help="Upper limit for prime constants C (default: 10000)")
    parser.add_argument("--sequence_limit", type=int, default=100, help="Number of terms for Fibonacci, Lucas, and Pell sequences (default: 100)")
    parser.add_argument("--mersenne_limit", type=int, default=50000, help="Upper limit for Mersenne test values of p (default: 50000)")
    args = parser.parse_args()
    
    # Call generate_primes with parsed arguments
    generate_primes(c_limit=args.c_limit, sequence_limit=args.sequence_limit, mersenne_limit=args.mersenne_limit)
