while True:
	for noun in range(100):
		for verb in range(100):
			with open('data.txt', 'r') as f:
				token_stream  = f.read()
				tokens = token_stream.split(',')
				tokens[1] = noun
				tokens[2] = verb
				instruction_pointer = 0
				opcode = tokens[instruction_pointer]
				while not (opcode == '99'):
					if opcode == '1' or opcode == 1:
						tokens[int(tokens[instruction_pointer+3])] = int(tokens[int(tokens[instruction_pointer+1])]) + int(tokens[int(tokens[instruction_pointer+2])])
						instruction_pointer += 4
					elif opcode == '2' or opcode == 2:
						tokens[int(tokens[instruction_pointer+3])] = int(tokens[int(tokens[instruction_pointer+1])]) * int(tokens[int(tokens[instruction_pointer+2])])
						instruction_pointer += 4
					opcode = tokens[instruction_pointer]
				if tokens[0] == 19690720:
					print(noun* 100 + verb)
					print('we found it at', noun, verb)