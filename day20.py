from day20inputs import inputs

lines = inputs[1].split()
enhancement = lines[0]

input_image = []

for line in lines[1:]:
    input_image.append(line)


def pad(input_image, step):
    fill = '.' if step % 2 == 0 else enhancement[0] 
    next_input_image = [fill * (len(input_image) + 10)] * 5 
    for line in input_image:
        next_input_image.append(fill * 5 + line + fill *5)
    next_input_image += [fill * (len(input_image) + 10)] * 5 
    return next_input_image

def define(i ,j):
    binary = input_image[i-1][j-1:j+2] + \
            input_image[i][j-1:j+2] + input_image[i+1][j-1:j+2]
    binary = binary.replace('.', '0').replace('#', '1')
    idx = int(binary, 2)
    e = enhancement[idx]
    return e

print sum([item.count('#') for item in input_image])

for step in range(50):
    input_image = pad(input_image, step)

    output_image = []
    for i in range(1, len(input_image) - 1):
        output_row = ''
        for j in range(1, len(input_image[0]) - 1):
            output_row += define(i, j)
        output_image.append(output_row)
    input_image = output_image 

for i in input_image:
    print i

print sum([item.count('#') for item in input_image])
print len(input_image), len(input_image[0])

