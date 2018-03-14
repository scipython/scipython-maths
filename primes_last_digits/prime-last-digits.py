import time
import math

# Prime numbers greater than 5 end in 1, 3, 7 or 9. It seems that a prime
# ending in one digit is less likely to be followed by another ending in the
# same digit. Return a dictionary summarizing this distribution. More details
# at https://scipython.com/blog/do-consecutive-primes-avoid-sharing-the-same-last-digit/
# Christian Hill, March 2016.

def approx_nth_prime(n):
    """Return an upper bound for the value of the nth prime"""

    return n * (math.log(n) + math.log(math.log(n)))

nmax = 10000000
pmax = approx_nth_prime(nmax)
print('The {:d}th prime is approximately {:d}'.format(nmax,int(pmax)))
N = int(math.sqrt(pmax)) + 1
print('Our sieve will therefore contain primes up to', N)

def primes_up_to(N):
    """A generator yielding all primes less than N."""

    yield 2
    # Only consider odd numbers up to N, starting at 3
    bsieve = [True] * ((N-1)//2)
    for i,bp in enumerate(bsieve):
        p = 2*i + 3
        if bp:
            yield p
            # Mark off all multiples of p as composite
            for m in range(i, (N-1)//2, p):
                bsieve[m] = False

gen_primes = primes_up_to(N)
sieve = list(gen_primes)

def is_prime(n, imax):
    """Return True if n is prime, else return False.

    imax is the maximum index in the sieve of potential prime factors that
    needs to be considered; this should be the index of the first prime number
    larger than the square root of n.

    """
    return not any(n % p == 0 for p in sieve[:imax])


digit_count = {1: {1: 0, 3: 0, 7: 0, 9: 0},
               3: {1: 0, 3: 0, 7: 0, 9: 0},
               7: {1: 0, 3: 0, 7: 0, 9: 0},
               9: {1: 0, 3: 0, 7: 0, 9: 0}}

# nprimes is the number of prime numbers encountered
nprimes = 0
# the most recent prime number considered (we start with the first prime number
# which ends with 1,3,7 or 9 and is followed by a number ending with one of
# these digits, 7 since 2, 3 and 5 are somewhat special cases.
last_prime = 7
# The current prime number to consider, initially the one after 7 which is 11
n = 11
# The index of the maximum prime in our sieve we need to consider when testing
# for primality: initially 2, since sieve[2] = 5 is the nearest prime larger
# than sqrt(11). plim is this largest prime from the sieve.
imax = 2
plim = sieve[imax]
start_time = time.time()

while nprimes <= nmax:
    # Output a progress indicator
    if not nprimes % 1000:
        print(nprimes)

    if is_prime(n, imax):
        # n is prime: update the dictionary of last digits
        digit_count[last_prime % 10][n % 10] += 1
        last_prime = n
        nprimes += 1
    # Move on to the next candidate (skip even numbers)
    n += 2

    # Update imax and plim if necessary
    if math.sqrt(n) >= plim:
        imax += 1
        plim = sieve[imax]
end_time = time.time()
print(digit_count)
print('Time taken: {:.2f} s'.format(end_time - start_time))
