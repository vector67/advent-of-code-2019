import sys
def resolve_parameters(tokens, immediate_modes, parameters):
	immediate_modes = list(immediate_modes)
	immediate_modes.reverse()
	# print('immediate', immediate_modes)
	for i in range(len(parameters)):
		if i >= len(immediate_modes) or int(immediate_modes[i]) == 0:
			parameters[i] = tokens[int(parameters[i])]
			# print()
	return parameters

def get_parameters(tokens, current_index, num_parameters):
	return [int(x) for x in tokens[current_index + 1: current_index + 1 + num_parameters]]

def get_parameters_and_resolve(tokens, current_index, num_parameters):
	opcode, immediate_modes = split_instruction(tokens[current_index])
	return [int(x) for x in resolve_parameters(tokens, immediate_modes, get_parameters(tokens, current_index, num_parameters))]

def split_instruction(token):
	return token[-2:], token[:-2]

with open('Day 5/data2.txt', 'r') as f:
	token_stream  = f.read()
	tokens = token_stream.split(',')
	current_index = 0
	opcode, immediate_modes = split_instruction(tokens[current_index])
	counter = 0
	while not (int(opcode) == 99): # and counter < 5:
		# print(tokens)
		# print(tokens[current_index], 'opcode', opcode, 'imm', immediate_modes)
		if int(opcode) == 1:
			# print('adding')
			parameters = get_parameters_and_resolve(tokens, current_index, 2)
			# print('parameters', parameters)
			tokens[int(tokens[current_index+3])] = str(parameters[0] + parameters[1])
			current_index += 4

		if int(opcode) == 2:
			# print('multiplying')
			parameters = get_parameters_and_resolve(tokens, current_index, 2)
			# print(parameters)
			tokens[int(tokens[current_index+3])] = str(parameters[0] * parameters[1])
			current_index += 4

		if int(opcode) == 3:
			print('input')
			parameters = get_parameters(tokens, current_index, 1)
			tokens[parameters[0]] = input("Please input a value: ")
			current_index += 2

		if int(opcode) == 4:
			# print('output')
			parameters = get_parameters(tokens, current_index, 1)
			immediate_modes = list(immediate_modes)
			if len(immediate_modes) > 0 and int(immediate_modes[0]) == 1:
				print('output: ', parameters[0])
			else:
				print('output: ', tokens[parameters[0]])
			current_index += 2

		opcode, immediate_modes = split_instruction(str(tokens[current_index]))
		counter += 1
		sys.stdout.flush()
	print(tokens)