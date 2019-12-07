import math
print()
sum_nums = 0
with open('data.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()

        current_num = int(line)
        print('')
        while int(math.floor(current_num/3)) - 2 > 0:
            new_num = int(math.floor(current_num/3)) - 2
            sum_nums += new_num
            current_num = new_num
            print(current_num)
        print('done')
    print(sum_nums)