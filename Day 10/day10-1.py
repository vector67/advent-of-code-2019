import math
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
print(map_asteroids)
# print((0,0) in map_asteroids)
best_other_asteroids = 0
for asteroid_pos, blocked_asteroids in map_asteroids.items():
    num_other_asteroids_seen = 0
    possible_winning_map = []
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
                    num_other_asteroids_seen += 1
                    possible_winning_map.append(other_asteroid)
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
                    num_other_asteroids_seen += 1
                    possible_winning_map.append(other_asteroid)

    print(asteroid_pos, num_other_asteroids_seen)
    if num_other_asteroids_seen > best_other_asteroids:
        best_other_asteroids = num_other_asteroids_seen
        winner_position = asteroid_pos
        winning_map = possible_winning_map
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
print(best_other_asteroids)
print(winner_position)