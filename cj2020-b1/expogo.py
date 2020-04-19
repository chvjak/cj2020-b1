# https://codingcompetitions.withgoogle.com/codejam/round/000000000019fef2/00000000002d5b62
# promising idea - analyse grid of points reachable from 0,0
# it is symmetric, so only 1/4 and possibly easy to obtain - i.e number are powers of 2 +/- 1
# reach X,Y using 1 + 2 + 4 + ... 2^i

f = open(r"expogo1.txt")

import sys        
#f = sys.stdin

def solve(N):

    res = ""
    return res


T = int(f.readline())

for t in range(T):
    X, Y = [int(x) for x in f.readline().split(" ")]
    res = solve(X, Y)  

    print ("Case #{0}: {1}".format(t + 1, res))
