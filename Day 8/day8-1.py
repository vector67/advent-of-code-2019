for line in open("Day 8/data.txt"):
    current_layer = []
    layers = [current_layer]
    counter = 0
    min_0s = 150
    final_output = -1
    sum_0s = 0
    for pixel in line:
        if counter >= 150:
            if sum_0s < min_0s:
                min_0s = sum_0s
                num_1s = 0
                num_2s = 0
                for i in current_layer:
                    if i == "1":
                        num_1s += 1
                    if i == "2":
                        num_2s += 1
                final_output = num_2s * num_1s
            counter = 0
            current_layer = []
            layers.append(current_layer)
            sum_0s = 0
        current_layer.append(pixel)
        if pixel == "0":
            sum_0s += 1
        counter += 1
    final_picture = [[2 for y in range(25)] for x in range(6)]
    for layer in layers:
        x = 0
        y = 0
        counter = 0
        for pixel in layer:
            x = counter % 25
            y = int(counter / 25)
            print(x, y)
            if final_picture[y][x] == 2:
                if not pixel == 2:
                    final_picture[y][x] = int(pixel)

            counter += 1
    print(final_picture)
    for row in final_picture:
        row_string = ""
        for pixel in row:
            if pixel == 0:
                row_string += " "
            else:
                row_string += str(pixel)
        print(row_string)
print(final_output)