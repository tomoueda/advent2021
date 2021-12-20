from day19inputs import inputs
lines = inputs[1].split('\n')

scanners = []
scanner = []
for line in lines[1:]:
    if '---' in line:
        scanners.append(scanner)
        scanner = []
    elif line == '':
        continue
    else:
        args = line.split(',')
        scanner.append(list(map(int, args)))
scanners.append(scanner)

from math import pi, cos, sin
from collections import Counter
def rotate_x(beacon, degree):
    x, y, z = beacon
    new_y = int(cos(degree)) * y - int(sin(degree)) * z 
    new_z = int(sin(degree)) * y + int(cos(degree)) * z
    return [x, new_y, new_z] 

def rotate_y(beacon, degree):
    x, y, z = beacon
    new_x = int(cos(degree)) * x + int(sin(degree)) * z 
    new_z = -int(sin(degree)) * x + int(cos(degree)) * z
    return [new_x, y, new_z]

def rotate_z(beacon, degree):
    x, y, z = beacon
    new_x = int(cos(degree)) * x - int(sin(degree)) * y 
    new_y = int(sin(degree)) * x + int(cos(degree)) * y
    return [new_x, new_y, z]
    
# Each has scanner unknown position, unknown rotation, unknown direction
# p = position, r = rotation, f = facing direction 

possible_r = [0, pi / 2, pi, -pi / 2]
possible_dir = {
        '+x': (rotate_y, 0, rotate_x),
        '-x': (rotate_z, pi, rotate_x),
        '+y': (rotate_z, pi / 2, rotate_y),
        '-y': (rotate_z, -pi / 2, rotate_y),
        '+z': (rotate_y, pi / 2, rotate_z),
        '-z': (rotate_y, -pi / 2, rotate_z)}

# compare the two scanners. If enough points line up return a transformation
# relative to scan0.
def compare(scan0, scan1):
    for name, transform in possible_dir.items():
        rotate, degree, axis_rotate = transform
        temp = list(map(lambda beacon: rotate(beacon, degree), list(scan1)))
        for r in possible_r:
            fresh = list(temp)
            fresh = list(map(lambda beacon: axis_rotate(beacon, r), fresh))
            counter = Counter()
            for p in scan0:
                for t in fresh:
                    counter[(int(p[0] - t[0]),
                        int(p[1] - t[1]), int(p[2] - t[2]))] += 1
            win = counter.most_common()[0]
            if win[1] >= 12:
                return name, r, win[0]

graph = {} 
for i in range(len(scanners)):
    for j in range(len(scanners)):
        if i == j:
            continue
        scan0 = list(scanners[i])
        scan1 = list(scanners[j])
        steps = compare(scan0, scan1)
        if steps is not None:
            if j not in graph:
                graph[j] = []
            graph[j].append((i, steps))

def operate(beacons, op):
    direction, axis_degree, translate = op
    rotate, degree, axis = possible_dir[direction] 
    t = list(map(lambda i: rotate(i, degree), beacons))
    t = list(map(lambda item: axis(item, axis_degree), t))
    return list(map(lambda i: (i[0] + translate[0], i[1] + translate[1], \
            i[2] + translate[2]), t))

# part 1
# beacons = set(map(lambda i : (i[0], i[1], i[2]), scanners[0]))

beacons = set([(0, 0, 0)])

for i in range(1, len(scanners)):
# part 1 
#   scanner = scanners[i]

    scanner = [(0, 0, 0)]
    stack = [(i, [])]
    visited = set()
    while len(stack) != 0:
        node, ops = stack.pop()
        if node not in visited:
            visited.add(node)
            for next_node, op in graph[node]:
                next_ops = list(ops)
                next_ops.append(op)
                if next_node == 0:
                    for o in next_ops:
                        scanner = operate(scanner, o)
                    for beacon in scanner:
                        beacons.add(beacon)
                    break
                else:
                    stack.append((next_node, next_ops))

print len(beacons)

# part 2
b = list(beacons)
largest = 0

for i in range(len(b) - 1):
    for j in range(i + 1, len(b)):
        scanA = b[i]
        scanB = b[j]
        largest = max(largest, abs(scanA[0] - scanB[0]) + \
                abs(scanA[1] - scanB[1]) + \
                abs(scanA[2] - scanB[2]))
print largest

