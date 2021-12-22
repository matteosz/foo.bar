#FIND LUCKY TRIPLES: DYNAMIC PROGRAMMING IS NEEDED TO STAY IN O(n^2)
# x divides y and y divides z, l list of positive integers

def solution(l):
    
    x = len(l)
    if x == 2: #x is in range [2,2000]
        return 0
    n = 0 #number of lucky triples
    c = [0] * x #counter-> c[i] indicates how many numbers before l[i] divide it
    for i in range(x):
        for j in range(i):
            if l[i] % l[j] == 0:
                c[i] += 1
                n += c[j]
            
    
    return n

l1 = [1, 2, 3, 4, 5, 6]
l2 = [1,1,1]
print(solution(l1) == 3)
print(solution(l2)== 1) 