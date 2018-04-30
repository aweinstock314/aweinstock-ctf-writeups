from hashlib import sha256
import math
import os
import gmpy
'''
def produire_key(k):
    p = getPrime(k)
    n = p ** 3
    while True:
        g = getRandomRange(1, n-1)
        g_p = pow(g, p-1, p**2)
        if pow(g_p, p, p**2) == 1:
            break
    h0 = getRandomRange(1, n-1)
    h = pow(h0, n, n)
    pubkey = (n, g, h)
    return pubkey

def crypter(m, pubkey):
    n, g, h = pubkey
    Mlen = len(bin(bytes_to_long(m))[2:])
    k = len(bin(n)[2:])/3
    rlen = getRandomRange(1, k - Mlen)
    R = long_to_bytes(getRandomInteger(rlen))
    r = bytes_to_long(sha256(m + R).digest())
    c = (pow(g, bytes_to_long(m + R), n) * pow(h, r, n)) % n
    return c
'''

def randint(numbits):
    assert numbits % 8 == 0, str(numbits)
    return int(os.urandom(numbits/8).encode('hex'), 16)

def randprime(numbits):
    return gmpy.next_prime(randint(numbits))

def randunder(x):
    while True:
        y = randint(int(math.ceil(gmpy.bit_length(x)/8.0)*8))
        if 0 < y < x:
            return y

def bytes_to_long(s):
    x = 0
    while len(s):
        x <<= 8
        x += ord(s[0])
        s = s[1:]
    return x

def long_to_bytes(x):
    s = ''
    while x > 0:
        s += chr(x & 0xff)
        x >>= 8
    return s[::-1]

assert all(bytes_to_long(long_to_bytes(i)) == i for i in range(0x1000))

def keygen(k=2048):
    p = randprime(k)
    q = randprime(k)
    n = p**3
    #n = p*p*q
    while True:
        g = randunder(p)
        g_p = pow(g, p-1, p**2)
        if pow(g_p, p, p**2) == 1:
            break
    h0 = randunder(n)
    h = pow(h0, n, n)
    pubkey = (n, g, h)
    privkey = (p, g_p)
    return pubkey, privkey

def encrypt(m, pubkey):
    n, g, h = pubkey
    Mlen = len(bin(bytes_to_long(m))[2:])
    k = len(bin(n)[2:])/3
    rlen = randunder(k - Mlen)
    R = long_to_bytes(randint(int(math.ceil(rlen/8.0)*8)))
    r = bytes_to_long(sha256(m + R).digest())
    a, b = pow(g, bytes_to_long(m + R), n), pow(h, r, n)
    c = (a * b) % n
    return c, r, R, a, b

"""
count = 0
for _ in range(50):
    pub, priv = keygen()
    ctxt, r, R = encrypt('FLAGFLAGFLAGFLAG', pub)

    from cuberoot import cuberoot
    assert priv[0] == cuberoot(pub[0])

    p = priv[0]
    inv = gmpy.invert(r, p*(p-1))
    print(repr(inv))
    if inv != 0:
        count += 1
    
'''
>>> 16.0/50
0.32
'''
'''
>>> 21.0/50
0.42
'''
"""
pub, priv = keygen(2048)
ctxt, r, R, a, b = encrypt('FLAG'*8, pub)

"""
from cuberoot import cuberoot
assert priv[0] == cuberoot(pub[0])

p = cuberoot(pub[0])
g = pub[1]
g_p = pow(g, p-1, p**2)

h = pub[2]
h0 = priv[2]
inv = gmpy.invert(r, p*(p-1))
inv2 = gmpy.invert(priv[2], p**3)
#print(repr(inv), repr(inv2))
#print((ctxt * gmpy.invert(p*p*(p-2)*r, p*(p-1))) % (p**3))
"""

def fixpoint(f, x):
    y = f(x)
    i = 0
    while x != y:
        print(x,y)
        x, y = y, f(y)
        i += 1
        if i % 10000 == 0:
            print i
    return x

#z = fixpoint(lambda x: (x*(pow(priv[2], 1, p**3)))%(p**3), ctxt)
"""
z = ctxt
count = 0
#tmp = (h0 ** p) % (p**3)
tmp = (inv2 ** p) % (p**3)
while z != a:
    #z *= inv2
    z *= tmp
    z %= p**3
    count += 1
    if count >= 0x50000:
        print 'failed'
        break
"""

def dlog(y, g, m):
    '''
>>> [(i, dlog(i, 3, 17)) for i in range(18)]
[(0, None), (1, 16), (2, 14), (3, None), (4, 12), (5, 5), (6, 15), (7, 11), (8, 10), (9, 2), (10, 3), (11, 7), (12, 13), (13, 4), (14, 9), (15, 6), (16, 8), (17, None)]
>>> [(i, dlog(i, 5, 17)) for i in range(18)]
[(0, None), (1, 16), (2, 6), (3, 13), (4, 12), (5, None), (6, 3), (7, 15), (8, 2), (9, 10), (10, 7), (11, 11), (12, 9), (13, 4), (14, 5), (15, 14), (16, 8), (17, None)]
    '''
    x, tmp = 1, g
    while tmp != 1:
        x, tmp = x+1, (tmp*g)%m
        if tmp == y:
            return x
    return None
    
n, g, h = pub
p, g_p = priv

# https://pdfs.semanticscholar.org/1f66/6ce3b6f365c5711246f4319fd8d65e7e83f0.pdf 2.2.3
#div = lambda a,b: a/b
div = lambda a,b: (a*gmpy.invert(b, p))
#l = lambda x: div(x-1, p)
#l = lambda a: pow(a-1, (p-1)/2, p)
l = lambda x: (x-1)/p
c_p = pow(ctxt, p-1, p*p)
x = div(l(c_p), l(g_p)) % p
print(repr(long_to_bytes(x)))
