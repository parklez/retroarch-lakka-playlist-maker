with open('MAME 0.233 - Split.dat', 'r') as f:
    lines = f.readlines()
    i = 0
    for line in lines:
        if line.startswith('	_name '):
            del lines[i]
        i += 1

with open('result.dat', 'w+') as f2:
    for line in lines:
        f2.write(line)
