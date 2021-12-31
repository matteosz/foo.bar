#DFS solution: 3 tests passed, 3rd and 5th fail
import math
def is_loop(m,n):
    # by induction, we see there's a loop if y = (2^n - 1)x (e.g. y=3x,y=7x,y=15x,y=63x...)
    # however, this is true only if we can guarantee y>x and they never swap.
    # More in general we say there's a loop if x*k = (2^n - k)*y -> k*(x+y)=2^n * y -> (k/y)(x+y) = pow(2)
    z = (m + n) // math.gcd(m,n)
    # Check if z is a power of 2:
    # If we subtract a power of 2 numbers by 1 then all unset bits after the only set bit become set; and the set bit become unset.
    # So, if a number n is a power of 2 then bitwise & of n and n-1 will be zero.
    return bool((z - 1) & z)
    

def create_graph(banana_list):
    # adjacenty list implementation
    G = {i:[] for i in range(len(banana_list))}
    for i in range(len(banana_list)):
        for j in range(i,len(banana_list)):
            if banana_list[i]!=banana_list[j] and is_loop(banana_list[i],banana_list[j]):
                G[i].append(j)
                G[j].append(i)
        
    return G

def custom_dfs(G,i,seen,pair):
    seen[i] = True
    n = 0
    for j in G[i]:
        if seen[j] is False:
            n += custom_dfs(G,j,seen,pair)

    if pair[0] is False:
        pair[0] = True
        return n
    else: 
        pair[0] = False
        return n+2

def find_max_lt(G):
    # we need to find the max value of connected pairs
    n = 0
    seen = [False] * len(G)
    for i in range(len(G)):
        if seen[i] is False:
            n += custom_dfs(G,i,seen,[False])
    return n

def solution(banana_list):
    # create a graph where a vertex represents a trainer
    # and edges the matches with a loop
    # we can implement it as adjacency list

    G = create_graph(banana_list)

    # now we apply a matching algorithm to the graph

    return len(banana_list)-find_max_lt(G)  


print(solution([1,1]))
print(solution([1, 7, 3, 21, 13, 19]))
print(solution([1]))
print(solution([1, 7, 1, 1]))
