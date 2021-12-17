inputs = []
inputs.append('target area: x=20..30, y=-10..-5')
inputs.append('target area: x=56..76, y=-162..-134')

line = inputs[1]
args = line.split()
x_range = args[2].split('..')
lower_x = int(x_range[0][2:])
upper_x = int(x_range[1][:-1])
y_range = args[3].split('..')
lower_y = int(y_range[0][2:])
upper_y = int(y_range[1])

import sys

def within_target(x, y):
    return upper_x >= x >= lower_x and upper_y >= y >= lower_y

def launch(x, y):
    pos = (0, 0)
    hit = False
    height = 0
    while pos[1] > lower_y and pos[0] < upper_x:
        pos = (pos[0] + x, pos[1] + y)
        height = max(height, pos[1])
        hit = hit or within_target(pos[0], pos[1])
        if x > 0:
            x -= 1
        elif x < 0:
            x += 1
        y -= 1
    return hit, height

global_max = 0
count = 0
for i in range(1000):
    for j in range(-1000, 1000):
        hit, local_max = launch(i, j)
        if hit:
            count += 1
            global_max = max(global_max, local_max)


