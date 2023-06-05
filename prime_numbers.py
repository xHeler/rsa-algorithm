import random
import psutil

from temperature import get_cpu_temperature

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def find_big_primes(start, end):
    primes = []
    if start % 2 == 0:
        start += 1
    for num in range(start, end + 1, 2):
        if is_prime(num):
            primes.append(num)
            if len(primes) == 2:
                return primes[0], primes[1]

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
    random_int = random.randint(1, 1024) * 10**3 + get_cpu_temperature()
    p, q = find_big_primes(random_int, random_int + 10000)
    print(f"p = {p}, q = {q}")
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi)
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))