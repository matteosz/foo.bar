def solution1(l,t):#O(n^2), still passes all tests

    for i in range(len(l)):
        for j in range(i,len(l)):
            if sum(l[i:j+1]) == t:
                return [i,j]
    return [-1,-1]

def solution2(l,t):#optimized version
    i,j = 0,0
    while i<=j and j<len(l):
        s = sum(l[i:j+1])
        if s == t:
            return [i,j]
        if s < t:#try to shift ahead the ending index to reach the wanted sum
            j += 1
        else:#s>t -> we have to start from the next index, j holds its value if after i 
            i += 1
            j = max(i,j)

    return [-1,-1]

l = [[1, 2, 3, 4],[4, 3, 10, 2, 8]]
t = [15,12]
print(solution2(l[0],t[0]))
print(solution2(l[1],t[1]))