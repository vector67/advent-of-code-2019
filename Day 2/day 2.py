with open('data.txt', 'r') as f:
	token_stream  = f.read()
	tokens = token_stream.split(',')
	current_index = 0
	opcode = tokens[current_index]
	while not (opcode == '99'):
		if opcode == '1' or opcode == 1:
			tokens[int(tokens[current_index+3])] = int(tokens[int(tokens[current_index+1])]) + int(tokens[int(tokens[current_index+2])])
		if opcode == '2' or opcode == 2:
			tokens[int(tokens[current_index+3])] = int(tokens[int(tokens[current_index+1])]) * int(tokens[int(tokens[current_index+2])])
		current_index += 4
		opcode = tokens[current_index]
	print(tokens)