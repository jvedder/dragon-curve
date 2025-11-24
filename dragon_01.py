def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

dragon = [1]
for i in range(10):
    dragon = dragon + [1] + [-n for n in dragon[::-1]]
    print(i, dragon)
    
move = [ (0,1), (-1,0), (0,-1), (1,0) ]
pos = (0,0)
dir = 0

with open('dragon.txt', 'w') as f:
    f.write('LR, dir, x, y\n')
    for x in dragon:
        dir = (dir + x) % 4
        pos = add(pos, move[dir])
        f.write(str(x))
        f.write(', ')
        f.write(str(dir))        
        f.write(', ')
        f.write(str(pos[0]))
        f.write(', ')
        f.write(str(pos[1]))
        f.write('\n')
