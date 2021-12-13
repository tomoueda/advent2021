from day13_inputs import inputs

lines = inputs[1].split()
points = set() 
folds = []
for line in lines:
    if ',' in line:
        points.add(tuple(map(int, line.split(','))))
    if '=' in line:
        fold = line.split('=')
        folds.append((fold[0], int(fold[1])))

# part 1
# axis, value = folds[0]
# print axis, value
# folded_points = set()
# for point in points:
#     pivot = point[0] if axis == 'x' else point[1]
#     if pivot > value:
#         newval = None
#         if axis == 'x':
#             diff = abs(point[0] - value)
#             newval = (value - diff, point[1])
#         if axis == 'y':
#             diff = abs(point[1] - value)
#             newval = (point[0], value - diff)
#         folded_points.add(newval)
#     else:
#         folded_points.add(point)


for fold in folds:
    axis, value = fold
    folded_points = set()
    for point in points:
        pivot = point[0] if axis == 'x' else point[1]
        if pivot > value:
            newval = None
            if axis == 'x':
                diff = abs(point[0] - value)
                newval = (value - diff, point[1])
            if axis == 'y':
                diff = abs(point[1] - value)
                newval = (point[0], value - diff)
            folded_points.add(newval)
        else:
            folded_points.add(point)
    points = folded_points

max_x = 0
max_y = 0

for point in points:
    max_x = max(max_x, point[0])
    max_y = max(max_y, point[1])

for i in range(max_x + 1):
    r = ''
    for j in range(max_y + 1):
        if (i, j) in points:
            r += 'x'
        else:
            r += ' '
    print r


