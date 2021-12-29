def solution(x, y):
    # Instead going from 1,1 to x,y and explore all solutions
    # we start directly from x,y and we make steps to come to 1,1

    # Everytime the greater number will subtract all possible multiples of the other
    count = 0
    M, F = int(x),int(y)

    while min(M,F) > 1:
        
        div = max(M,F) // min(M,F) - (1 if max(M,F) % min(M,F) == 0 else 0)
        count += div
        if M > F:
            M %= F
        else: 
            F %= M

    return 'impossible' if min(M,F) != 1 else str(count + max(M,F) - 1)

m, n = '2', '1'
print(solution(m,n))
m, n = '4', '7'
print(solution(m,n))

