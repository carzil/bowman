def bfs(y, x, op, m, n, n2, mas, go):
    ma = [x for x in range(1000)]
    if x - 1 > -1 and y - 1 > -1:
        if m[y - 1][x - 1] != '*':
            if m[y - 1][x - 1] == op:
                go[y - 1][x - 1] = [y, x]
                return m, mas, go, True, [y - 1, x - 1], m[y][x] + 1
            if m[y - 1][x - 1] not in ma:
                m[y - 1][x - 1] = m[y][x] + 1
                mas.append([y - 1, x - 1])
                go[y - 1][x - 1] = [y, x]
    if x - 1 != -1:
        if m[y][x - 1] != '*':
            if m[y][x - 1] == op:
                go[y][x - 1] = [y, x]
                return m, mas, go, True, [y, x - 1], m[y][x] + 1
            if m[y][x - 1] not in ma:
                m[y][x - 1] = m[y][x] + 1
                mas.append([y, x - 1])
                go[y][x - 1] = [y, x]
    if y - 1 != -1:
        if m[y - 1][x] != '*':
            if m[y - 1][x] == op:
                go[y - 1][x] = [y, x]
                return m, mas, go, True, [y - 1, x], m[y][x] + 1
            if m[y - 1][x] not in ma:
                m[y - 1][x] = m[y][x] + 1
                mas.append([y - 1, x])
                go[y - 1][x] = [y, x]
    if x + 1 < n and y + 1 < n2:
        if m[y + 1][x + 1] != '*':
            if m[y + 1][x + 1] == op:
                go[y + 1][x + 1] = [y, x]
                return m, mas, go, True, [y + 1, x + 1], m[y][x] + 1     
            if m[y + 1][x + 1] not in ma:
                m[y + 1][x + 1] = m[y][x] + 1
                mas.append([y + 1, x + 1])
                go[y + 1][x + 1] = [y, x]
    if x + 1 < n:
        if m[y][x + 1] != '*':
            if m[y][x + 1] == op:
                go[y][x + 1] = [y, x]
                return m, mas, go, True, [y, x + 1], m[y][x] + 1
            if m[y][x + 1] not in ma:
                m[y][x + 1] = m[y][x] + 1
                mas.append([y, x + 1])
                go[y][x + 1] = [y, x]
    if y + 1 < n2:
        if m[y + 1][x] != '*':
            if m[y + 1][x] == op:
                go[y + 1][x] = [y, x]
                return m, mas, go, True, [y + 1, x], m[y][x] + 1
            if m[y + 1][x] not in ma:
                m[y + 1][x] = m[y][x] + 1
                mas.append([y + 1, x])
                go[y + 1][x] = [y, x]
    if y - 1 > -1 and x + 1 < n:
        if m[y - 1][x + 1] != '*':
            if m[y - 1][x + 1] == op:
                go[y - 1][x + 1] = [y, x]
                return m, mas, go, True, [y - 1, x + 1], m[y][x] + 1
            if m[y - 1][x + 1] not in ma:
                m[y - 1][x + 1] = m[y][x] + 1
                mas.append([y - 1, x + 1])
                go[y - 1][x + 1] = [y, x]
    if x - 1 > -1 and y + 1 < n2:
        if m[y + 1][x - 1] != '*':
            if m[y + 1][x - 1] == op:
                go[y + 1][x - 1] = [y, x]
                return m, mas, go, True, [y + 1, x - 1], m[y][x] + 1
            if m[y + 1][x - 1] not in ma:
                m[y + 1][x - 1] = m[y][x] + 1
                mas.append([y + 1, x - 1])
                go[y + 1][x - 1] = [y, x]
    return m, mas, go, False, [], 0
matrix = [['.' for i in range(10)] for j in range(10)]
matrix[4][4] = '*'
matrix[3][4] = '*'
matrix[1][2] = 0
matrix[7][8] = 'b'
m = matrix
go = [[[] for x in range(10)] for y in range(10)]
n, n2 = 10, 10
mas = [[1, 2]]
for i in range(n * n2):
    m, mas, go, b, res, ras = bfs(mas[i][0], mas[i][1], 'b', m, n, n2, mas, go)
    if b == True:
        break
r = [res]
for i in range(ras):
    r.append(go[res[0]][res[1]])
    res = go[res[0]][res[1]]
print(res, ras)
for i in range(len(m)):
    m[i] = list(map(str, m[i]))
    m[i] = ' '.join(m[i])
m = '\n'.join(m)
for i in range(len(go)):
    go[i] = list(map(str, go[i]))
    go[i] = ' '.join(go[i])
go = '\n'.join(go)
print(m)
print(go)
print(r)
a = input()