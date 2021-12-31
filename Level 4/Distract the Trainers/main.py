def gcd(m,n):#Euclidian's algorithm
    if n==0:
        return m
    return gcd(n,m%n)

def is_loop(m,n):
    # by induction, we see there's a loop if y = (2^n - 1)x (e.g. y=3x,y=7x,y=15x,y=63x...)
    # however, this is true only if we can guarantee y>x and they never swap.
    # More in general we say there's a loop if x*k = (2^n - k)*y -> k*(x+y)=2^n * y -> (k/y)(x+y) = pow(2)
    z = (m + n) // gcd(m,n)
    # Check if z is a power of 2:
    # If we subtract a power of 2 numbers by 1 then all unset bits after the only set bit become set; and the set bit become unset.
    # So, if a number n is a power of 2 then bitwise & of n and n-1 will be zero.
    return bool((z - 1) & z)  

def create_graph(banana_list):
    # adjacenty list implementation with dictionary for faster operations
    G = {i:[] for i in range(len(banana_list))}
    for i in range(len(banana_list)):
        for j in range(i,len(banana_list)):
            if banana_list[i]!=banana_list[j] and is_loop(banana_list[i],banana_list[j]):
                G[i].append(j)
                G[j].append(i)
        
    return G

def remove(G, x):#used to remove and mark trainers as processed 
    for i in range(len(G)):
        j = 0 
        while j < len(G[i]):
            if(G[i][j]==x):
                G[i].pop(j)
            j+=1 
    G[x]=[-1]

def find_max_lt(G):
    to_process=len(G)
    left = 0
    while(to_process>0):

        # find the trainer with less connections (possibly not zero)
        min_num=0 # first shot trainer0
        for i in range(1,len(G)):
            if (len(G[i])<len(G[min_num]) or G[min_num]==[-1]) and G[i]!=[-1]:
                min_num=i
        # if the trainer has no connection and it hasn't been removed yet
        if len(G[min_num])==0 and G[min_num]!=[-1]:
            remove(G, min_num)
            to_process-=1
            left+=1
        else:# else find the one connected to him with less connections and remove them both as pair
            min_node=G[min_num][0]
            for i in range(1,len(G[min_num])):
                if G[min_num][i]!=min_num and len(G[G[min_num][i]])<len(G[min_node]):
                    min_node=G[min_num][i]
            if G[min_node]!=[-1]:
                remove(G, min_num)
                remove(G, min_node)
                to_process-=2

    return left

def solution(banana_list):
    # create a graph where a vertex represents a trainer
    # and edges the matches with a loop
    # we can implement it as adjacency list
    G = create_graph(banana_list)
    # now we apply a matching algorithm to the graph
    return find_max_lt(G)  


print(solution([1,1]))
print(solution([1, 7, 3, 21, 13, 19]))
print(solution([1]))
print(solution([1, 7, 1, 1]))

