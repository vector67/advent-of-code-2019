def is_valid_password(password):
	has_double = False
	previous_num = -1
	previous_previous_num = -1
	counter = 0
	for character in str(password):
		if int(character) < previous_num:
			return False
		if int(character) == previous_num
			and not(int(character) == previous_previous_num) \
			and not ((counter <= len(str(password)) - 2) and str(password)[counter + 1] == character):
			has_double = True
		previous_previous_num = previous_num
		previous_num = int(character)
		counter += 1
	return has_double

start = 134792
end = 675810
sum_passwords = 0
for test_password in range(start, end + 1):
	if is_valid_password(test_password):
		sum_passwords += 1
print(is_valid_password(112233))
print(is_valid_password(123444))
print(is_valid_password(111134))
print(sum_passwords)