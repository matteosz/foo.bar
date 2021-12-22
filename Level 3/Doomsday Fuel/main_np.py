#Markov Chains and absorbing states - Theory required
from fractions import Fraction
import numpy as np

def get_transition_matrix(m,absorbing,non_absorbing):
    p = [] #in order to use MARKOV CHAINS it's important to have separated absorbing states from non-absorbing ones
    row = absorbing + non_absorbing

    for i, rowNumber in enumerate(absorbing):
        p.append(m[rowNumber])
        p[i][i] = 1

    for nonAbsorbingI in non_absorbing:
        orderedRow = []
        for orderI in row:
            orderedRow.append(m[nonAbsorbingI][orderI])
        fractionRow = []
        for col in orderedRow:
            fractionRow.append(col/ float(sum(orderedRow)))
        p.append(fractionRow)

    return p

def extract_matrices(m,t,s):
    q,r = [],[]
    for row in range(s, s+t):
        q.append(m[row][s:])
        r.append(m[row][:s])

    return q,r

def get_fundamental_matrix(q,t):
    return np.linalg.inv(np.subtract(np.identity(t),q))

def get_result(m,s):
    num,den = [],[]
    res = [0] * (s+1) #absorbing states + denominator
    mcm = 1
    for i in range(s):
        x = Fraction(m[i]).limit_denominator()#simplify the fraction
        num.append(x.numerator)
        den.append(x.denominator)
        mcm = np.lcm(mcm,x.denominator)

    res[s] = mcm

    for i in range(s):
        res[i] = int(mcm/den[i]) * num[i]

    return res

def solution(m):
    l = len(m)
    absorbing_order,non_absorbing_order = [],[]

    for i, row in enumerate(m):
        if(max(row) == 0):
            absorbing_order.append(i)
        else:
            non_absorbing_order.append(i)

    s = len(absorbing_order)#absorbing states number
    t = l - s

    if s == 1:#s0 is an absorbing state
        return [1, 1]
    
    transition_matrix = get_transition_matrix(m,absorbing_order,non_absorbing_order)
    #extract Q and R after reordering
    # TM = | ID  0 | Q is t x t, R is t x s
    #      | R   Q |
    q, r = extract_matrices(transition_matrix,t,s)
    #compute N = (Id - Q)^-1
    n = get_fundamental_matrix(q,t)
    #finally compute M = N R, M_ij contains prob of being absorbed in state j after starting from state i
    # we do focus only on i=0 considering we start always from s0: column M_0j
    m = np.dot(n,r)
    #
    #find common denominator and convert to result format
    res = get_result(m[0],s)
    return res

m = [
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
s = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]
print(solution(s))
print(solution(m))
