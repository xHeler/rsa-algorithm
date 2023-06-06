from random import randrange, getrandbits, randint

def power(a, d, n):
    ans = 1
    while d != 0:
        if d % 2 == 1:
            ans = ((ans % n) * (a % n)) % n
        a = ((a % n) * (a % n)) % n
        d >>= 1
    return ans


def MillerRabin(N, d):
    a = randrange(2, N - 1)
    x = power(a, d, N)
    if x == 1 or x == N - 1:
        return True
    else:
        while d != N - 1:
            x = ((x % N) * (x % N)) % N
            if x == 1:
                return False
            if x == N - 1:
                return True
            d <<= 1
    return False


def is_prime(N, K):
    if N == 3 or N == 2:
        return True
    if N <= 1 or N % 2 == 0:
        return False
    d = N - 1
    while d % 2 != 0:
        d /= 2

    for _ in range(K):
        if not MillerRabin(N, d):
            return False
    return True


def generate_prime_candidate(length):
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p


def generatePrimeNumber(length):
    A = 4
    while not is_prime(A, 128):
        A = generate_prime_candidate(length)
    return A

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(e, phi):
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % phi

def generate_keypair():
    length = 15  # Decrease the length of the prime numbers
    p = generatePrimeNumber(length)
    q = generatePrimeNumber(length)    
    n = p * q
    phi = (p - 1) * (q - 1)
    e = randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = randint(2, phi)
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))