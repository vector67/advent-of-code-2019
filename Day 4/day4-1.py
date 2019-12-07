# print(sum([(all(i <= j for i, j in zip(str(x), str(x)[1:]))) for x in range(134792, 675811)]))
print(sum([(sorted(str(x)) == list(str(x)) and not all(i < j for i, j in zip(str(x), str(x)[1:])) and all(i == j and j == k for i, j, k in zip(str(x), str(x)[1:], str(x)[2:]))) for x in range(134792, 675811)]))
# for x in range(1000, 2000):
# 	print(x, all(i <= j for i, j in zip(str(x), str(x)[1:])))
sum_passwords = 0
for test_password in range(134792, 675811):
	has_double = False
	test_password = str(test_password)
	for i in range(1, len(test_password)):
		if test_password[i] < test_password[i-1]:
			has_double = False
			break
		elif test_password[i] == test_password[i-1]:
			has_double = True
	if has_double:
		sum_passwords += 1
print(sum_passwords)
