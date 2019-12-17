import math
import random
import time
import sys
def get_visible_from(asteroid_pos):
    visible_asteroids = []
    for other_asteroid, other_blocked_asteroids in map_asteroids.items():
        if not (asteroid_pos == other_asteroid):
            StartX = asteroid_pos[0]
            StartY = asteroid_pos[1]
            EndX = other_asteroid[0]
            EndY = other_asteroid[1]
            m = 0.0;

            run = EndX - StartX
            if run == 0:
                if StartY > EndY:
                    temp = StartY
                    StartY = EndY
                    EndY = temp
                found_one = False
                for y in range(StartY + 1, EndY):
                    if (StartX, y) in map_asteroids:
                        found_one = True
                        break
                if not found_one:
                    visible_asteroids.append(other_asteroid)
            else:
                rise = EndY - StartY
                m = rise* 1.0 / run * 1.0
                # solve for b
                # (start with y = mx + c, subtract mx from both sides)
                c = StartY - (m * StartX)

                if StartX > EndX:
                    temp = StartX
                    StartX = EndX
                    EndX = temp
                found_one = False
                for x in range(StartX + 1, EndX):
                    y = m*x + c
                    if y.is_integer() or y - math.floor(y) < 0.001 or math.ceil(y) - y < 0.001:
                        y = round(y)
                        if (x, y) in map_asteroids:
                            found_one = True
                            break
                    # if asteroid_pos[0] == 47 and asteroid_pos[1] == 1:
                    #     print(y, m, x, c, found_one, other_asteroid[0], other_asteroid[1])
                if not found_one:
                    visible_asteroids.append(other_asteroid)
    return visible_asteroids

def get_angles_of_asteroids(laser_pos, visible_asteroids):
    angles = []
    for asteroid_pos in visible_asteroids:
        angle_to_append = math.atan2((asteroid_pos[1] - laser_pos[1]), (asteroid_pos[0] - laser_pos[0])/2)
        
        angles.append(angle_to_append + math.pi*2)
        # if random.random() < 0.001:
        # print(angles[-1], laser_pos,  asteroid_pos)
    return angles
map_asteroids = {}
x = 0
y = 0
for line in open('Day 10/data.txt'):
    x = 0
    for pixel in line:
        if pixel == "#":
            map_asteroids[(x, y)] = []
        x += 1
    width = x
    y += 1
height = y
# print(map_asteroids)
# print((0,0) in map_asteroids)
best_other_asteroids = 0
for asteroid_pos, blocked_asteroids in map_asteroids.items():
    possible_winning_map = get_visible_from(asteroid_pos)
    num_other_asteroids_seen = len(possible_winning_map)
    if num_other_asteroids_seen > best_other_asteroids:
        best_other_asteroids = num_other_asteroids_seen
        winner_position = asteroid_pos
        winning_map = possible_winning_map

def print_state(winner_position, winning_map, map_asteroids):
    for y in range(height):
        print_str = ""
        for x in range(width):
            if (x,y) == winner_position:
                print_str += "A"
            elif (x, y) in winning_map:
                print_str += "#"
            elif (x,y) in map_asteroids:
                print_str += "a"
            else:
                print_str += "."
        print(print_str)
# print_state(winner_position, winning_map, map_asteroids)
# print(best_other_asteroids)
print(winner_position)
laser_pos = winner_position
counter = 0
current_angle = math.pi*3/2 - 0.0001
while counter < 200:
    visible_asteroids = get_visible_from(laser_pos)
    angles = get_angles_of_asteroids(laser_pos, visible_asteroids)
    current_smallest_angle = math.pi*2
    current_winner = -1
    for i in range(len(angles)):
        if angles[i] - current_angle < current_smallest_angle and angles[i] > current_angle:
            current_smallest_angle = angles[i] - current_angle
            current_winner = i
    if current_winner == -1:
        current_angle -= math.pi*2
        print("had to continue")
        continue
    # if counter == 199:
    print('num ', counter + 1, ' is ', visible_asteroids[current_winner], current_smallest_angle)
    map_asteroids.pop(visible_asteroids[current_winner], None)
    current_angle = angles[current_winner]
    print_state(visible_asteroids[current_winner], visible_asteroids, map_asteroids)
    sys.stdout.flush()
    time.sleep(0.1)
    counter += 1