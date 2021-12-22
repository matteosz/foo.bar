def solution(n, b):

    v = list()
    v.append(int(n,base=b))
    k = len(n)
    while True:
        x = int("".join(sorted(n, reverse=True)), base=b)
        y = int("".join(sorted(n)), base=b)
        tmp = x - y
        
        for i in range(len(v)):
            if v[i] == tmp:#cycle
                return len(v) - i

        if tmp <= 0:#constant
            return 1
        v.append(tmp)
        n = ""
        for i in range(k):
            if tmp == 0:
                n += '0'
            else:
                r = tmp % b
                n += str(r)
            tmp = int(tmp / b)
        n = n[::-1] #reverse string

s = '1211'
b = 10
print(solution(s,b))

#221100-
#001122=
#212201