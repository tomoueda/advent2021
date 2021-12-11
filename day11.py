inputs = []
inputs.append("""5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""")

inputs.append("""6318185732
1122687135
5173237676
8754362612
5718474666
8443654137
1247634346
1446514585
6717288267
1727871228""")

lines = inputs[1].split()
graph = []
for line in lines:
    row = []
    for char in line:
        row.append(int(char))
    graph.append(row)

def neighbors(i, j):
    if i - 1 >= 0:
        yield (i - 1, j)
    if j - 1 >= 0:
        yield (i, j - 1)
    if i - 1 >= 0 and j - 1 >= 0:
        yield (i - 1, j - 1)
    if i + 1 != len(graph):
        yield (i + 1, j)
    if j + 1 != len(graph[0]):
        yield (i, j + 1)
    if i + 1 != len(graph) and j + 1 != len(graph[0]):
        yield (i + 1, j + 1)
    if i - 1 >= 0 and j + 1 != len(graph[0]):
        yield (i - 1, j + 1)
    if i + 1 != len(graph) and j - 1 >= 0:
        yield (i + 1, j - 1)

def increase_all():
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            graph[i][j] += 1

def flash(i, j):
    for i, j in neighbors(i, j):
        graph[i][j] += 1


# c = 0
# step = 100 
# part 1
# while step > 0:
#     increase_all()
#     stack = []
#     visited = set() 
#     for i in range(len(graph)):
#         for j in range(len(graph[0])):
#             if graph[i][j] > 9:
#                 stack.append((i, j))
#     while len(stack) != 0:
#         coord = stack.pop()
#         if coord not in visited:
#             visited.add(coord)
#             i, j = coord 
#             flash(i, j)
#             for i2, j2 in neighbors(i, j):
#                 if graph[i2][j2] > 9:
#                     stack.append((i2, j2))
#     for i, j in visited:
#         graph[i][j] = 0
#     c += len(visited) 
#     step -= 1

step = 0
visited = set() 
while len(visited) != len(graph) * len(graph[0]):
    step += 1
    increase_all()
    stack = []
    visited = set() 
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] > 9:
                stack.append((i, j))
    while len(stack) != 0:
        coord = stack.pop()
        if coord not in visited:
            visited.add(coord)
            i, j = coord 
            flash(i, j)
            for i2, j2 in neighbors(i, j):
                if graph[i2][j2] > 9:
                    stack.append((i2, j2))
    for i, j in visited:
        graph[i][j] = 0
