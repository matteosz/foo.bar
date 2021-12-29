#This solution exceeds time limit!

def dfs(x,y,cases,n,target_x,target_y):

    if x == target_x and y == target_y:
        return n
 
    n1 = 'impossible'
    n2 = 'impossible'
    m = int(x)
    f = int(y)

    if m+f <= int(target_x):# pruning condition
        n1 = dfs(str(m+f),y,cases,n+1,target_x,target_y)
    if m+f <= int(target_y):
        n2 = dfs(x,str(m+f),cases,n+1,target_x,target_y)

    if n1 == 'impossible':
        return n2
    if n2 == 'impossible':
        return n1
    return min(n1,n2)
    

def solution(x, y):

    # we parametrize the two bombs as a string "MF"
    # if I return 
    cases = set()
    ans = dfs('1','1',cases,0,x,y)
    
    return str(ans)





m, n = '2', '1'
print(solution(m,n))
m, n = '4', '7'
print(solution(m,n))