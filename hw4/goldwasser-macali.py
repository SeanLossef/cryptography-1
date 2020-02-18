#!/usr/bin/env python
# encoding: utf8
from unicodedata import normalize 
from string import ascii_letters
from random import randint
import sys

# Miller-Rabin probabilistic primality test (HAC 4.24)
# returns True if n is a prime number
# n is the number to be tested
# t is the security parameter


def miller_rabin(n, t):
    assert(n % 2 == 1)
    assert(n > 4)
    assert(t >= 1)

    # select n - 1 = 2**s * r
    r, s = n - 1, 0
    while r % 2 == 0:
        s += 1
        r >>= 1 #r = (n - 1) / 2 ** s

    for i in range(t):
        a = randint(2, n - 2) # this requires n > 4

        y = pow(a, r, n) # python has built-in modular exponentiation
        if y != 1 and y != n - 1:
            j = 1
            while j <= s - 1 and y != n - 1:
                y = pow(y, 2, n)
                if y == 1:
                    return False
                j += 1
            if y != n - 1:
                return False

    return True

def is_prime(n):
    if n in [2, 3]:
        return True
    if n % 2 == 0:
        return False

    return miller_rabin(n, 10)

def nearest_prime(n):
    if is_prime(n):
        return n

    if n % 2 == 0:
        n += 1

    i = 0
    while True:
        i += 1
        n += 2

        if is_prime(n):
            return n 

def big_prime(size):
    n = randint(1, 9)
    for s in range(size):
        n += randint(0, 9) * s**10

    return nearest_prime(n)

def is_even(x):
    return x % 2 == 0

# calculates jacobi symbol (a n)
def jacobi(a, n):
    if a == 0:
        return 0
    if a == 1:
        return 1

    e = 0
    a1 = a
    while is_even(a1):
        e += 1
        a1 /= 2
    assert 2**e * a1 == a

    s = 0

    if is_even(e):
        s = 1
    elif n % 8 in {1, 7}:
        s = 1
    elif n % 8 in {3, 5}:
        s = -1

    if n % 4 == 3 and a1 % 4 == 3:
        s *= -1

    n1 = n % a1
    
    if a1 == 1:
        return s
    else:
        return s * jacobi(n1, a1)

def quadratic_non_residue(p):
    a = 0
    while jacobi(a, p) != -1:
        a = randint(1, p)

    return a

def xeuclid(a, b):
    """ return gcd(a,b), x and y in 'gcd(a,b) = ax + by'.
    """
    x = [1, 0]
    y = [0, 1]
    sign = 1
 
    while b:
        q, r = divmod(a, b)
        a, b = b, r
        x[1], x[0] = q*x[1] + x[0], x[1]
        y[1], y[0] = q*y[1] + y[0], y[1]
        sign = -sign
 
    x = sign * x[0]
    y = -sign * y[0]
    return a, x, y
 
 
def gauss_crt(a, m):
    """ return x in ' x = a mod m'.
    """
    modulus = reduce(lambda a,b: a*b, m)
 
    multipliers = []
    for m_i in m:
        M = modulus / m_i
        gcd, inverse, y = xeuclid(M, m_i)
        multipliers.append(inverse * M % modulus)
 
    result = 0
    for multi, a_i in zip(multipliers, a):
        result = (result + multi * a_i) % modulus
    return result

def pseudosquare(p, q):
    a = quadratic_non_residue(p)
    b = quadratic_non_residue(q)

    return gauss_crt([a, b], [p, q])

def generate_key(prime_size = 6):
    p = big_prime(prime_size)
    q = big_prime(prime_size)
    # p = 13
    # q = 11
    while p == q:
        p2 = big_prime(prime_size)

    y = pseudosquare(p, q)
    n=p*q
    
    keys = {'pub': (n, y), 'priv': (p, q)}
    return keys

def int_to_bool_list(n):
    return [b == "1" for b in "{0:b}".format(n)]

def bool_list_to_int(n):
    s = ''.join(['1' if b else '0' for b in n])
    return int(s, 2)

def encrypt(m, pub_key):
    bin_m = int_to_bool_list(m)
    n, y = pub_key

    def encrypt_bit(bit):
        x = randint(0, n)
        if bit:
            return (y * pow(x, 2, n)) % n
        return pow(x, 2, n)
    return map(encrypt_bit, bin_m)

def decrypt(c, priv_key):
    p, q = priv_key
    def decrypt_bit(bit):
        e = jacobi(bit, p)
        if e == 1:
            return False
        return True

    m = map(decrypt_bit, c)
    return bool_list_to_int(m)

def normalize_str(s):
    u = unicode(s, 'utf8')
    valid_chars = ascii_letters + ' '
    un = ''.join(x for x in normalize('NFKD', u) if x in valid_chars).upper()
    return un.encode('ascii', 'ignore')

def int_encode_char(c):
    ind = ord(c)
    val = 27 # default value is space

    # A-Z: A=01, B=02 ... Z=26
    if ord('A') <= ind <= ord('Z'):
        val = ind - ord('A') + 1

    return "%02d" % val

def int_encode_str(s):
    return int(''.join(int_encode_char(c) for c in normalize_str(s)))

message='abcd'

key = generate_key()
print key
m = int_encode_str(message)
print "\nMessage:",message, "Encoded:",m 
enc = encrypt(m, key['pub'])
print "\nEncrypted:",enc
dec = decrypt(enc, key['priv'])
print "\nDecrypted:",dec