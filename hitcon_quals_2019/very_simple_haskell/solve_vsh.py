# I appended the following to the provided `prob.hs` to more cleanly get intermediate values out of ghci
'''
-- premagic is the challenge's magic function with the final call to calc removed, for turning a string into bits of the correct endianness
premagic input = result
    where 
        num = stringToInteger input
        bits = numToBits num
        extended = reverse $ extendBits 8 bits
        oriLen = length extended
        extendedBits = extendBits k extended
        oriLenBits = numToBits $ fromIntegral oriLen
        extendedOriLenBits = extendBits k oriLenBits
        finalBits = extendedOriLenBits ++ extendedBits
        result = reverse finalBits

-- recursively split a list into length-i chunks (since calc works in 131-bit blocks)
recSplit i [] = []
recSplit i s = let (a, b) = splitAt i s in a : recSplit i b

input c = "the flag is hitcon{" ++ replicate 6 c ++ "}"
[a, b, c] = recSplit 131 (premagic (input '\0'))
'''
import gmpy

primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739]

a = [0,1,1,1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0,0,1,1,0,0,0,0,1,0,1,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,1,0,1,1,1,0,0,1,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,0,1,0,1,1,1,0,1,0,0,0,1,1,0,0,0,1,1,0,1,1]
b = [0,1,1,1,1,0,1,1,0,1,1,1,0,0,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
c = [0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

n = 134896036104102133446208954973118530800743044711419303630456535295204304771800100892609593430702833309387082353959992161865438523195671760946142657809228938824313865760630832980160727407084204864544706387890655083179518455155520501821681606874346463698215916627632418223019328444607858743434475109717014763667

# (calc 1 x) runs the calculation for a single block of bits, which encodes the bitvector into a single number; since (product primes) < n, there is no information loss
# if x, y, z are distinct blocks, (calc 1 x ^ 4) * (calc 1 y ^ 2) * (calc 1 z) == calc 1 (x ++ y ++ z), since there's squaring in the recursion
# the squaring allows us to determine the order of the blocks, consider the following examples for 4-bit blocks:
# (calc 1 ([0,1,1,0] ++ [0,1,1,1])) would give us (2^0)*(3^2)*(5^2)*(7^1) with no squaring, making it indistinguishable from (calc 1 ([0,1,1,1]++[0,1,1,0]))
# with squaring, the former is (2^0)*(3^3)*(5^3)*(7^1), and the latter would be (2^0)*(3^3)*(5^3)*(7^2)
calc_a = 70998196091606985545993711787111356453960854621421971918477501437269263801218145273626982609030910240112248874611888516366214608505
calc_b = 1474740362480446660394438995826744655
calc_c = 3553

def solve(given):
    # since the reductions are modulo n, we can't read off the result from the final block since the higher powers are truncated
    # but since n is coprime to the first 131 primes, and since we know the first and last blocks, we can cancel them mod n and preserve the powers in the middle block
    # and then read off the bits of the middle block by gcding the encoding with each of the primes
    middle = (gmpy.invert(calc_a**4, n) * given * gmpy.invert(calc_c, n)) % n
    # unsure why this works without taking a square root of middle first
    bits = []
    for i in range(131):
        bits.append(1 if gmpy.gcd(middle, primes[i]) != 1 else 0)
    candidates = []
    # check each offset, because the the 131-bit boundary between the first two blocks is in the middle of the 'o' in "hitcon"
    for offset in range(8):
        bytes_ = []
        for i in range(131/8):
            bytes_.append(chr(sum(bit*2**(7-idx) for (idx, bit) in enumerate(bits[offset+8*i:offset+8*(i+1)]))))
        candidates.append(''.join(bytes_))
    # we know the flag is surrounded by curly braces
    return [c for c in candidates if c.find('{') < c.find('}')]

output = 84329776255618646348016649734028295037597157542985867506958273359305624184282146866144159754298613694885173220275408231387000884549683819822991588176788392625802461171856762214917805903544785532328453620624644896107723229373581460638987146506975123149045044762903664396325969329482406959546962473688947985096

print(solve(output))
