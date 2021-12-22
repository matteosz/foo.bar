def answer(data,n):

    distinct = set(data)
    for x in distinct:
        if data.count(x) > n:
            data = list(filter(lambda y : y != x, data))

    return data

data = [[1, 2, 3],[1, 2, 2, 3, 3, 3, 4, 5, 5],[1, 2,3]]
n = [0,1,6]
print(answer(data[0],n[0]))
print(answer(data[1],n[1]))
print(answer(data[2],n[2]))