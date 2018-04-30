#!/usr/bin/env python
# given f, f', f'', find x s.t. f(x) = 0
def halley(f, fprime, fprimeprime, x0=1):
    'https://en.wikipedia.org/wiki/Halley%27s_method'
    x = x0
    while not f(x) == 0:
        x = x - ((2*f(x)*fprime(x)) / (2*(fprime(x)**2) - f(x)*fprimeprime(x)))
    return x

# given n, compute n**(1/3) as the value satisfying (x**3 - n = 0)
def cuberoot(n):
    # f(x) = x**3 - n
    # f'(x) = 3x**2 - 0
    # f''(x) = 6x
    return halley(lambda x: x*x*x-n, lambda x: 3*x*x, lambda x: 6*x)

cuberoot_correct = lambda i: cuberoot(i**3) == i
assert all(cuberoot_correct(i) for i in range(1,1000))
assert all(cuberoot_correct(1 << i) for i in range(990, 1000))
