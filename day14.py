from day14_inputs import inputs

lines = inputs[1].split('\n')
template = [a for a in lines[0]]
memo = {}
for line in lines[1:]:
    pair, insert = line.split('->')
    memo[pair.strip()] = insert.strip()

from collections import Counter

c = Counter(template)


# part 1
# steps = 40
# while steps > 0:
# 
#     insert_idx = 1
#     next_step_template = list(template)
#     for i in range(len(template)):
#         if i == len(template) - 1:
#             break
#         pair = template[i] + template[i+1]
#         insert_c = memo[pair]
#         c[insert_c] += 1
#         next_step_template.insert(insert_idx, insert_c)
#         insert_idx += 2 
#     template = next_step_template
#     steps -= 1
# 
# commons = c.most_common()
# print commons[0][1] - commons[-1][1]

pair_counts = Counter() 

for i in range(len(template)):
    if i == len(template) - 1:
        break
    pair = template[i] + template[i+1]
    pair_counts[pair] += 1

steps = 40 
c = Counter(template)

while steps > 0:
    next_pair_count = Counter()
    for pair, count in pair_counts.most_common():
        insert_c = memo[pair]
        c[insert_c] += count
        next_pair_count[pair[0] + insert_c] += count 
        next_pair_count[insert_c + pair[1]] += count 
    pair_counts = next_pair_count
    steps -= 1

commons = c.most_common()
print commons[0][1] - commons[-1][1]
