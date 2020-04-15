def minimum(a, b, c):
    if a < b:
        if a < c:
            return a
        else:
            return c
    else:
        if b < c:
            return b
        else:
            return c
def mini(a):
    mini1 = a[0]
    for i in a:
        if mini1 > i:
            mini1 = i
    return mini1
def sort(a):
    for i in range(len(a) - 1):
        for j in range(i, len(a)):
            if a[i] > a[j]:
                temp = a[i]
                a[i] = a[j]
                a[j] = temp
    return a
def cost1(a):
    mini1 = mini(a)
    sum1 = 0
    for i in range(len(a)):
        if a[i] != mini1:
            sum1 += a[i]
    sum1 += (len(a) - 2) * mini1
    return sum1
def cost2(a):
    large = len(a) - 1
    i = 0
    sum2 = 0
    while large > 2:
        if i % 2 == 0:
            sum2 += a[0] + a[1]
        else:
            sum2 += a[large] + a[1]
            large -= 2
        i += 1
    if large == 1:
        sum2 += a[1]
    elif large == 2:
        sum2 += a[0] + a[1] + a[2]
    return sum2
def cost3(a, sumx):
    if len(a) <= 0:
        return sumx
    elif len(a) == 2:
        sumx += a[0] + a[1]
        return sumx
    b = []
    i = 0
    sumx = 0
    while i < len(a) - 1:
        sumx += a[i] + a[i + 1]
        b.append(a[i])
        i += 2
    return cost3(b, sumx)
def cost(a):
    costa = cost1(a)
    costb = cost2(a)
    costc = cost3(a, 0)
    return minimum(costa, costb, costc)
t = int(input())
for i in range(t):
    n = int(input())
    a = list(map(int, input().strip().split()))
    a = sort(a)
    print(a)
    print(cost(a))