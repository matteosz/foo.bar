#MARKOV CHAINS and absorbing states - theory
from fractions import Fraction

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

def get_submatrix(m,i,j):
    sub = []
    for x in m[:i]+m[i+1:]:
        l = []
        for y in x[:j]+x[j+1:]:
            l.append(y)
        sub.append(l)
    return sub

def get_determinant(q):
    l = len(q)
    if l == 2:
        return q[0][0]*q[1][1] - q[0][1]*q[1][0]

    det = 0
    for i in range(l):
        det += ((-1)**i) * q[0][i] * get_determinant(get_submatrix(q,0,i))

    return det

def get_transpose(m):
    mt = []
    r = len(m)
    if r > 0:
        c = len(m[0])
        for j in range(c):
            l = []
            for i in range(r):
                l.append(m[i][j])
            mt.append(l)

    return mt

def get_inverse(q):
    det = get_determinant(q)

    if len(q) == 2:
        return [[q[1][1]/det, -1*q[0][1]/det],
                [-1*q[1][0]/det, q[0][0]/det]]

    cofactors = []
    for r in range(len(q)):
        cofactorRow = []
        for c in range(len(m)):
            cofactorRow.append(((-1)**(r+c)) * get_determinant(get_submatrix(q,r,c)))
        cofactors.append(cofactorRow)
    cofactors = get_transpose(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] /= det
    return cofactors

def multiply_matrices(n,r):
    prod = []
    x1,x2 = len(n),len(r)

    if x1>0 and x2>0 and len(n[0])==x2:
        x3 = len(r[0])
        for i in range(x1):
            tmp = []
            for j in range(x3):
                tot = 0
                for k in range(x2):
                    tot += n[i][k]*r[k][j]
                tmp.append(tot)
            prod.append(tmp)

    return prod

def get_fundamental_matrix(q,t):
    for i in range(t):
        for j in range(t):
            k = 0
            if i == j:
                k = 1
            q[i][j] = k - q[i][j]
    # Q -> Id_t - Q
    
    inv = get_inverse(q) # Q^-1
    
    return inv

def get_mcm(a,b):
    m = max([a,b])
    while m % a != 0 or m % b != 0:
        m += 1
    return m

def get_result(m,s):
    num = []
    den = []
    res = [0] * (s+1)
    mcm = 1
    for i in range(s):
        x = Fraction(m[i]).limit_denominator()
        num.append(x.numerator)
        den.append(x.denominator)
        mcm = get_mcm(mcm,x.denominator)

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
    
    if len(absorbing_order) == 1:
        return [1, 1]

    s = len(absorbing_order)
    t = l - s
    transition_matrix = get_transition_matrix(m,absorbing_order,non_absorbing_order)
    #extract Q and R
    # 
    # TM = | Q   R | Q is t x t, R is t x s
    #      | 0  ID |
    q, r = extract_matrices(transition_matrix,t,s)
    #compute N = (Id - Q)^-1
    n = get_fundamental_matrix(q,t)
    #finally compute M = N R, M_ij contains prob of being absorbed in state j after starting from state i
    # we do focus only on i=0! column M_0j

    m = multiply_matrices(n,r) #np.dot(n,r)

    #equalize m denominators before and converting to result
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