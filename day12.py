inputs = []

inputs.append("""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""")

inputs.append("""start-co
ip-WE
end-WE
le-ls
wt-zi
end-sz
wt-RI
wt-sz
zi-start
wt-ip
YT-sz
RI-start
le-end
ip-sz
WE-sz
le-WE
le-wt
zi-ip
RI-zi
co-zi
co-le
WB-zi
wt-WE
co-RI
RI-ip""")

inputs.append("""start-A
start-b
A-c
A-b
b-d
A-end
b-end""")

import re
from collections import Counter
lines = inputs[1].split()

graph = {}
def add_to_graph(key, val):
    if key not in graph:
        graph[key] = []
    graph[key].append(val)

for line in lines:
    nodes = line.split('-')
    add_to_graph(nodes[0], nodes[1])
    add_to_graph(nodes[1], nodes[0])

stack = [('start', [])]
c = []

# part 1
# while len(stack) != 0:
#     node, curr_path = stack.pop() 
#     m = re.findall('[a-z]', node)
#     if len(m) != 0 and node in curr_path:
#         continue
#     for path in graph[node]:
#         next_path = list(curr_path)
#         next_path.append(node)
#         if path == 'end':
#             c.append(next_path)
#         else:
#             stack.append((path, next_path))


def is_small_cave(node):
    m = re.findall('[a-z]', node)
    return len(m) != 0

def can_visit(node, curr_path):
    if node == 'start' and node in curr_path:
        return False 
    if not is_small_cave(node):
        return True
    if node not in curr_path:
        return True
    count = Counter(filter(is_small_cave, curr_path)).most_common(1)
    if count == []:
        return True
    return count[0][1] != 2
    

while len(stack) != 0:
    node, curr_path = stack.pop() 
    m = re.findall('[a-z]', node)
    if not can_visit(node, curr_path):
        continue
    for path in graph[node]:
        next_path = list(curr_path)
        next_path.append(node)
        if path == 'end':
            c.append(next_path)
        else:
            stack.append((path, next_path))
