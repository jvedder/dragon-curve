# --------------------------------------------------------------------
# Copyright (c) 2025 John Vedder
# MIT License
#
# This code is based in part on a Facebook post by Louis Kenneth Reinitz:
# https://www.facebook.com/groups/tiling/permalink/1978304919259710
# --------------------------------------------------------------------

iterations = 6
chamfer = 0.291
precision = 3

import matplotlib.pyplot as plt

# move the (x,y) point 'pt' by 'step' amount in 'dir' direction
# returns the new point (x,y)
def move(pt, step, dir):
    (x,y) = pt
    match dir:
        case 0:
            # north
            y = round(y + step, precision)
        case 1:
            # west
            x = round(x - step, precision)
        case 2:
            # south
            y = round(y - step, precision)
        case 3:
            # east
            x = round(x + step, precision)
    return (x,y)

# Build the dragon curve with
#   bend LEFT (L)  = +1
#   bend RIGHT (R) = -1
# Dragon curve iteration is:
#   D(0) = L
#   D(1) = D(0)+L-D(0)
#   D(n) = D(n-1)+L-D(n-1)
# where -D(n) means to swap L and R and reverse the order
# so the sequence is:
# L -> LLR -> LLRLLRR -> LLRLLRRLLLRRLRR -> ...

dragon = [1]
print('iteration', 'point_count')
for i in range(iterations):
    dragon = dragon + [1] + [-n for n in dragon[::-1]]
    print(i, len(dragon))

# Build the Twin Dragon Curve, which forms a closed loop
# from the Dragon Curve
# T(n) = D(n)+L+D(n)+L
# so the sequence is:
# LLLL -> LLRLLLRL -> LLRLLRRLLLRLLRRL -> ...
twin = dragon + [1] + dragon + [1]

# Generate points in curve with a chamfer in each corner.
# dir=0,1,2,3 means North, West, South, East
# Turn Left by adding 1 to dir, Right by subtracting 1 from dir
pos = (0,0)
dir = 0
points = [ ]
for d in twin:
    # chamfer from previous point 
    points.append( move(pos, chamfer, dir) )
    # chamfer to next point
    points.append( move(pos, 1-chamfer, dir) )
    # move to the next point
    pos = move(pos,  1, dir)
    # turn left or right
    dir = (dir + d) % 4
#close the Twin Dragon curve --last point = first point
points.append(points[0])

# Output the points as a CSV file -- you can plot as (x,y) in Excel
with open('dragon.txt', 'w') as f:
    f.write('x, y\n')
    for p in points:
        f.write(str(p[0]))
        f.write(', ')
        f.write(str(p[1]))  
        f.write('\n')

# Utility to plot the points with an offset
def plot_offset(points, offset):
    x = [p[0] + offset[0] for p in points]
    y = [p[1] + offset[1] for p in points]
    plt.plot(x, y, 'black')
    plt.fill(x, y)

# enumerate all offsets in x and y
match iterations:
    case 4:
        offsets_x = [-8,0,8]
        offsets_y = [-4,0,4]
    case 5:
        offsets_x = [-8,0,8]
        offsets_y = [-8,0,8]
    case 6:
        offsets_x = [-8,0,8]
        offsets_y = [-16,0,16]
    case _:
        #default case
        offsets_x = [0]
        offsets_y = [0]
offsets = []
for x in offsets_x:
    for y in offsets_y:
        offsets.append( (x,y) )

# set the plot color order 
plt.rcParams['axes.prop_cycle'] = plt.cycler('color', ['red','green','blue','orange','yellow'])

# plot the curve with offsets
for offset in offsets:
    plot_offset(points, offset)

plt.show()
