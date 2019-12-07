directions_x = {
    'R':1,
    'L':-1,
    'U':0,
    'D':0
}
directions_y = {
    'R':0,
    'L':0,
    'U':1,
    'D':-1
}
print('')
def get_wire_from_line(line):
    tokens = line.split(',')
    wire = [[0,0]]
    current_location = [0,0]
    for token in tokens:
        direction = token[0]
        distance = int(token[1:])
        new_location = [0, 0]
        new_location[0] = current_location[0] + distance*directions_x[direction]
        new_location[1] = current_location[1] + distance*directions_y[direction]
        wire.append(new_location)
        current_location = new_location
    return wire

def get_intersection_points(point1, point2, wire):
    going_right_or_left12 = abs(point1[0] - point2[0])
    intersections = []
    for i in range(1, len(wire)):
        pointa = wire[i - 1]
        pointb = wire[i]
        going_right_or_leftab = abs(pointa[0] - pointb[0])
        if not((going_right_or_leftab > 0 and going_right_or_left12 > 0) or (going_right_or_leftab == 0 and going_right_or_left12 == 0)):
            # print('intersection', point1, point2, pointa, pointb)
            if going_right_or_leftab > 0:
                if point1[0] > pointa[0] and point1[0] < pointb[0] and ((pointa[1] < point1[1] and pointa[1] > point2[1]) or (pointa[1] < point2[1] and pointa[1] > point1[1])):
                    intersections.append([point1[0], pointa[1]])
                elif point1[0] > pointb[0] and point1[0] < pointa[0] and ((pointa[1] < point1[1] and pointa[1] > point2[1]) or (pointa[1] < point2[1] and pointa[1] > point1[1])):
                    intersections.append([point1[0], pointa[1]])
                # else:
                #     print('no intersection')
            else:
                if pointa[0] > point1[0] and pointa[0] < point2[0] and ((point1[1] < pointa[1] and point1[1] > pointb[1]) or (point1[1] < pointb[1] and point1[1] > pointa[1])):
                    intersections.append([pointa[0], point1[1]])
                elif pointa[0] > point2[0] and pointa[0] < point1[0] and ((point1[1] < pointa[1] and point1[1] > pointb[1]) or (point1[1] < pointb[1] and point1[1] > pointa[1])):
                    intersections.append([pointa[0], point1[1]])
                # else:
                #     print('no intersection')
    return intersections

def within(x, x1, x2):
    return (x < x1 and x > x2) or (x > x1 and x < x2)
def calculate_single_wire_distance(intersection, wire):
    distance_thus_far = 0
    for i in range(1, len(wire)):
        pointa = wire[i - 1]
        pointb = wire[i]
        going_right_or_leftab = abs(pointa[0] - pointb[0])
        if going_right_or_leftab > 0:
            if pointa[1] == intersection[1] and within(intersection[0], pointa[0], pointb[0]):
                return distance_thus_far + abs(pointa[0] - intersection[0])
            distance_thus_far += going_right_or_leftab
        else:
            if pointa[0] == intersection[0] and within(intersection[1], pointa[1], pointb[1]):
                return distance_thus_far + abs(pointa[1] - intersection[1])
            distance_thus_far += abs(pointa[1] - pointb[1])
def calculate_wire_distance(intersection_point_x, intersection_point_y, wire1, wire2):
    return calculate_single_wire_distance((intersection_point_x, intersection_point_y), wire1) + calculate_single_wire_distance((intersection_point_x, intersection_point_y), wire2) 

with open('data.txt', 'r') as f:
    line1 = f.readline()
    line2 = f.readline()
    wire1 = get_wire_from_line(line1)
    wire2 = get_wire_from_line(line2)
    print(wire2)
    closest_intersection_point_distance = -1
    for i in range(1, len(wire1)):
        point1 = wire1[i - 1]
        point2 = wire1[i]
        intersection_points = get_intersection_points(point1, point2, wire2)
        if len(intersection_points) > 0:
            # print('got intersections', point1, point2, intersection_points)
            if closest_intersection_point_distance == -1:
                closest_intersection_point_distance = calculate_wire_distance(intersection_points[0][0], intersection_points[0][1], wire1, wire2)
            for intersection_point in intersection_points:
                manhattan_distance = calculate_wire_distance(intersection_points[0][0], intersection_points[0][1], wire1, wire2)
                if manhattan_distance < closest_intersection_point_distance:
                    closest_intersection_point_distance = manhattan_distance
    print(closest_intersection_point_distance)
    # print(wire1)