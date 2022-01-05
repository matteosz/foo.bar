from collections import Counter
def gcd(x,y):
    if y == 0:
        return x
    return gcd(y, x % y)
def factorial(n):#memorize all factorials required (from 0 to n)
    f = [1]
    for i in range(1,n+1):
        f.append(f[i-1]*i)
    return f        
def gcd_table(n):
    table = [[0 for _ in range(n+1)] for _ in range(n+1)] #all combinations
    for i in range(1,n+1):#don't compute for i nor j = 0, such they won't be used
        for j in range(i,n+1):
            table[i][j] = table[j][i] = gcd(i,j)
    return table
def generate_partitions(n):
        # generate partitions of the integer n
        # n -> FIRST
        # n-1 1
        # n-2 2
        # ......
        # 1 1 1 1 ...(n times) -> LAST
        partitions = []
        p = [0 for i in range(n)]
        p[0] = n #first partition -> element itself
        k = 0 #index of last element in the partition
        while True:
            partitions.append(p[:k+1])

            count = 0
            while k>=0 and p[k]==1:
                count += 1
                k -= 1

            if k<0:#all values are 1 -> no more partitions
                break
        
            p[k] -= 1
            count += 1

            while count>p[k]:
                p[k+1] = p[k]
                count -= p[k]
                k += 1
            
            p[k+1] = count
            k += 1

        return partitions
class Solution():
    def __init__(self,w,h,s):
        self.w = w
        self.h = h
        self.s = s
        # precompute once
        self.fcts = factorial(max(w,h))
        self.gcds = gcd_table(max(w,h))

    def get_cycle_idx(self,p,n):
        cycle = self.fcts[n]
        for i,x in Counter(p).items():
            cycle //= (i**x) * self.fcts[x]
        return cycle

    def solve(self):
        ans = 0
        for zw in generate_partitions(self.w):
            for zh in generate_partitions(self.h):
                z = self.get_cycle_idx(zw,self.w) * self.get_cycle_idx(zh,self.h)
                ab = [sum([self.gcds[i][j] for i in zw]) for j in zh]
                ans += z * self.s**(sum(ab))

        return ans//(self.fcts[self.w]*self.fcts[self.h])

def solution(w, h, s):
    sol = Solution(w,h,s)
    return str(sol.solve())


print(solution(2, 2, 2)) # 7
print(solution(2, 3, 4)) # 430