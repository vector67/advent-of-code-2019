import sys
def resolve_parameters(tokens, immediate_modes, parameters):
	list(immediate_modes).reverse()
	for i in range(len(parameters)):
		if i >= len(immediate_modes) or immediate_modes[i] == 0:
			parameters[i] = tokens[parameters[i]]
	return parameters

def get_parameters(tokens, current_index, num_parameters):
	return [int(x) for x in tokens[current_index + 1: current_index + 1 + num_parameters]]

def get_parameters_and_resolve(tokens, current_index, num_parameters):
	opcode, immediate_modes = split_instruction(tokens[current_index])
	return [int(x) for x in resolve_parameters(tokens, immediate_modes, get_parameters(tokens, current_index, num_parameters))]

def split_instruction(token):
	return token[-2:], token[:-2]

with open('data.txt', 'r') as f:
	token_stream  = f.read()
	tokens = token_stream.split(',')
	current_index = 0
	opcode, immediate_modes = split_instruction(tokens[current_index])
	counter = 0
	while not (int(opcode) == 99) and counter < 5:
		if int(opcode) == 1:
			parameters = get_parameters_and_resolve(tokens, current_index, 2)
			tokens[int(tokens[current_index+3])] = parameters[0] + parameters[1]
			current_index += 4

		if int(opcode) == 2:
			parameters = get_parameters_and_resolve(tokens, current_index, 2)
			tokens[int(tokens[current_index+3])] = parameters[0] * parameters[1]
			current_index += 4

		if int(opcode) == 3:
			parameters = get_parameters_and_resolve(tokens, current_index, 1)
			tokens[parameters[0]] = int(input("Please input a value: "))
			current_index += 2

		if int(opcode) == 4:
			parameters = get_parameters(tokens, current_index, 1)
			print(tokens[parameters[0]])
			current_index += 2

		opcode, immediate_modes = split_instruction(str(tokens[current_index]))
		print(opcode, immediate_modes)
		sys.stdout.flush()
	print(tokens)