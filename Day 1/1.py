import math
print()
sum_nums = 0
with open('data.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        print(line)
        sum_nums += math.floor(int(line)/3) - 2
    print(sum_nums)