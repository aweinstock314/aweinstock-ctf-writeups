from scipy.optimize import linprog
import numpy as np

#hashval = np.dot([31**2, 31, 1], [0, 104, 101])
#hashval = np.dot([31**2, 31, 1], [104, 101, 108])
#hashval = np.dot([31**4, 31**3, 31**2, 31, 1], list(map(ord, "hello")))

makepoly = lambda n: [31**(n-i-1) for i in range(n)]

#rawval = 'hello'
rawval = "hello world"
n = len(rawval)
poly = makepoly(n)
hashval = np.dot(poly, list(map(ord, rawval)))

# demonstration of setting up a linear program by hand, with explicit matrices
# we need an integer linear program though (since we can't set a byte to a fractional value), and scipy doesn't seem to have a solver for those
'''
x = linprog(
    c=[31**4, 31**3, 31**2, 31, 1],
    A_ub=[
        [1, 0, 0, 0, 0], # a <= 256
        [0, 1, 0, 0 ,0], # b <= 256
        [0, 0, 1, 0, 0], # c <= 256
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
        [-1, 0, 0, 0, 0], # -a <= 0 (i.e. a >= 0)
        [0, -1, 0, 0, 0], # -b <= 0 (i.e. b >= 0)
        [0, 0, -1, 0, 0], # -c <= 0 (i.e. c >= 0)
        [0, 0, 0, -1, 0],
        [0, 0, 0, 0, -1],
        [-31**4, -31**3, -31**2, -31, -1], # -ax**2 - bx - c <= -hashval
        [31**4, 31*3, 31**2, 31, 1], # ax**2 + bx + c <= hashval
    ],
    b_ub=[256, 256, 256, 256, 256, 0, 0, 0, 0, 0, -hashval, hashval]
    )
'''
x = linprog(c=poly,
    A_ub=np.vstack([np.eye(n, dtype=int), -np.eye(n, dtype=int), -np.array(poly, dtype=int), poly]),
    b_ub=[255]*n + [0]*n + [-hashval, hashval]
    )

print(x)

n = 6
hashval = 593779930 - (7*31**n) # the custom hash starts at 7 instead of 0, so subtract 7 at the first character
poly = makepoly(n)

import ctypes
glpk = ctypes.cdll['libglpk.so.40']
glpk.glp_create_prob.restype = ctypes.c_void_p
glpk.glp_add_cols.restype = ctypes.c_int
glpk.glp_add_cols.argtypes = [ctypes.c_void_p, ctypes.c_int]
glpk.glp_add_rows.restype = ctypes.c_int
glpk.glp_add_rows.argtypes = [ctypes.c_void_p, ctypes.c_int]
glpk.glp_set_col_bnds.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double]
glpk.glp_set_row_bnds.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double]
glpk.glp_set_mat_row.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)]
glpk.glp_simplex.restype = ctypes.c_int
glpk.glp_simplex.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
glpk.glp_print_sol.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
glpk.glp_intopt.restype = ctypes.c_int
glpk.glp_intopt.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
glpk.glp_print_mip.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
glpk.glp_set_col_kind.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
glpk.glp_mip_col_val.restype = ctypes.c_double
glpk.glp_mip_col_val.argtypes = [ctypes.c_void_p, ctypes.c_int]

# constants from /usr/include/glpk.h
GLP_FR = 1
GLP_LO = 2
GLP_IV = 2
GLP_DB = 4
GLP_FX = 5

def buf(ty, xs):
    'allocate a contiguous buffer of ctypes-values and store values from an iterable-with-length in it'
    r = (ty * len(xs))(0)
    for (i, x) in enumerate(xs):
        r[i] = x
    return r

prob = glpk.glp_create_prob()
# first n column vars are input bytes, last is a skolem variable (call it k) for modular congruence
colstart = glpk.glp_add_cols(prob, n+1)

for i in range(n):
    #glpk.glp_set_col_bnds(prob, colstart+i, GLP_DB, 0, 255.0)
    #glpk.glp_set_col_bnds(prob, colstart+i, GLP_DB, 0, 127.0) # 7-bit-clean
    #glpk.glp_set_col_bnds(prob, colstart+i, GLP_DB, ord(' '), ord('~')) # printable
    glpk.glp_set_col_bnds(prob, colstart+i, GLP_DB, ord('0'), ord('z')) # mostly alphanumeric

glpk.glp_set_col_bnds(prob, colstart+n, GLP_FR, 0, 0) # no constraints on k

rowstart = glpk.glp_add_rows(prob, 1)

# the row constraints essentially say `dot(poly, input) + k*(2**32) == hashval`
#glpk.glp_set_mat_row(prob, rowstart, 5, buf(ctypes.c_int, [0, 1, 2, 3, 4, 5]), buf(ctypes.c_double, [0.0, 31.0**4, 31.0**3, 31.0**2, 31.0, 1.0])) # explicitly constructed for length 5
#glpk.glp_set_mat_row(prob, rowstart, n, buf(ctypes.c_int, list(range(n+1))), buf(ctypes.c_double, [0.0]+poly)) # before the skolem variable was added
glpk.glp_set_mat_row(prob, rowstart, n+1, buf(ctypes.c_int, list(range(n+2))), buf(ctypes.c_double, [0.0]+poly+[1 << 32]))
glpk.glp_set_row_bnds(prob, rowstart, GLP_FX, hashval, hashval)

glpk.glp_simplex(prob, 0)
glpk.glp_print_sol(prob, ctypes.c_buffer("hasher_solution_simp.txt"))

for i in range(n+1):
    glpk.glp_set_col_kind(prob, colstart+i, GLP_IV) # all the variables need to be integer variables

glpk.glp_intopt(prob, 0)
glpk.glp_print_mip(prob, ctypes.c_buffer("hasher_solution_mip.txt"))

print(repr(''.join([chr(int(glpk.glp_mip_col_val(prob, colstart+i))) for i in range(n)])))
