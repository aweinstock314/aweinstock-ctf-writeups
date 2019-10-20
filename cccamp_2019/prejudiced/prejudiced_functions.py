from random import SystemRandom

R = SystemRandom()

def test(a, d, n, s):
    x = pow(a,d, n) 
    if x == 1 or x == n-1:
        return False

    for i in range(s):
        x = x*x % n
        if x == 1:
            return True
        if x == n-1:
            return False
    return True


def is_prime(n, rounds):
    if n % 2 == 0:
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    return not any(test(a, d, n, s) for a in R.sample(range(1,314), rounds))
