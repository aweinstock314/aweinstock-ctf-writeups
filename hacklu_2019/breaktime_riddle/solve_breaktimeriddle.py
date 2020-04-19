from pwn import *
import itertools
context.log_level = 'warn'

# the "ts =" line whilelists variable names/parens, and we don't have dot, so we can't eval arbitrary python
# in each round, we get 3 eval queries, and success in a round is being able to figure out which permutation of the functions in t1 was chosen
# recognized as https://qntm.org/gods / https://en.wikipedia.org/wiki/The_Hardest_Logic_Puzzle_Ever
# t1 corresponds to "always tells the truth"/identity, "always lies"/invert, "answers randomly"
# t2 corresponds to the "yes"/"no" "ja/da" mapping, by consistently choosing whether to invert the god's answer
# within the query, A/B/C are the god identities, X is 'does "ja" mean "yes"', and 0/1/2 are literal

def query(p, q):
    p.recvuntil('I?')
    p.sendline(q)
    reg = 'R: ([TF])'
    s = p.recvregex(reg)
    #print s
    r = {'T': 1, 'F': 0}[re.findall(reg, s)[0]]
    return r

idents = {k: {0,1,2} for k in "ABC"}
'''
p.recvuntil('I?')
p.sendline('0 ( X ) == ( A == 0 ) == ( B == 2 )')
x1 = p.recvuntil('I?')
r1 = {'T': 1, 'F': 0}[re.findall('R: ([TF])', x1)[0]]
'''

#for (foo, bar, baz) in list(itertools.product(*[[0,1]]*3)):
for (foo, bar, baz) in [(0, 1, 0)]:
    p = process('breaktime_riddle/public/riddle.py') if '--live' not in sys.argv else remote('breaktime-riddle.forfuture.fluxfingers.net', 1337)
    for i in range(50):
        print('%d %d %d: %d' % (foo, bar, baz, i))
        # debugging the extra set of parens took a while
        '''
        >>> False == False == False
        True
        >>> (False == False) == False
        False
        '''
        r1 = query(p, '0 ( ( X ) == ( A == 0 ) ) == ( B == 2 )')
        print('r1: %d' % (r1,))
        ask_b_or_c = {0: '2', 1: '1'}[r1]
        #p.sendline('2 ( X ) == ( 1 )')
        r2 = query(p, '%s X == 1' % (ask_b_or_c,))
        print('r2: %d' % (r2,))
        r3 = query(p, '%s ( X ) == ( A == 2 )' % (ask_b_or_c,))
        print('r3: %d' % (r3,))

        #foo, bar, baz = 1, 1, 1
        #baz = 0
        b, c = ('B', 'C') if r1 else ('C', 'B')
        if baz ^ r2:
            f = lambda x: 2 if x else 0
            idents = {'A': f(foo ^ r3), b: 1, c: f(1 ^ foo ^ r3)}
        else:
            f = lambda x: 2 if x else 1
            idents = {'A': f(bar ^ r3), b: 0, c: f(1 ^ bar ^ r3)}

        answer = '%d %d %d' % (idents['A'], idents['B'], idents['C'])
        print('answer: %r' % (answer,))

        p.recvuntil('A?')
        p.sendline(answer)

        s = p.recvregex('(W|C)')
        print(repr(s))
        if s[-1] == 'W':
            break

    print(p.recvall())

'''
'\nC'
orrect!
Good job, here is your flag: flag{Congr4ts_f0r_s0lving_The_Hardest_Logic_Puzzle_Ever}
'''
