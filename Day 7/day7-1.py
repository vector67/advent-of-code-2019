import sys
import itertools

def resolve_parameters(tokens, immediate_modes, parameters):
    immediate_modes = list(immediate_modes)
    immediate_modes.reverse()
    # print('immediate', immediate_modes)
    for i in range(len(parameters)):
        if i >= len(immediate_modes) or int(immediate_modes[i]) == 0:
            parameters[i] = tokens[int(parameters[i])]
            # print()
    return parameters
def yellow(text):
    return '\033[33m' + text + '\033[0m'
def get_parameters(tokens, current_index, num_parameters):
    return [int(x) for x in tokens[current_index + 1: current_index + 1 + num_parameters]]

def get_parameters_and_resolve(tokens, current_index, num_parameters):
    opcode, immediate_modes = split_instruction(tokens[current_index])
    return [int(x) for x in resolve_parameters(tokens, immediate_modes, get_parameters(tokens, current_index, num_parameters))]

def split_instruction(token):
    return token[-2:], token[:-2]

def pretty_print_tokens(tokens, current_index):
    output_string = ""
    for i in range(len(tokens)):
        index_string = "{:<2}".format(str(i))
        token_string = "{:<5}".format(str(tokens[i]))
        if i == current_index:
            index_string = yellow(index_string)
        output_string += index_string + ": " + token_string + "  "
        if i % 10 == 9: 
            output_string += "\n"
    print(output_string)

def run_program(tokens, input_array):
    output = []
    current_input_progress = 0
    current_index = 0
    opcode, immediate_modes = split_instruction(tokens[current_index])
    counter = 0
    while not (int(opcode) == 99):
        if int(opcode) == 1:
            parameters = get_parameters_and_resolve(tokens, current_index, 2)
            tokens[int(tokens[current_index+3])] = str(parameters[0] + parameters[1])
            current_index += 4

        if int(opcode) == 2:
            parameters = get_parameters_and_resolve(tokens, current_index, 2)
            tokens[int(tokens[current_index+3])] = str(parameters[0] * parameters[1])
            current_index += 4

        if int(opcode) == 3:
            parameters = get_parameters(tokens, current_index, 1)
            tokens[parameters[0]] = input_array[current_input_progress]
            current_input_progress += 1
            current_index += 2

        if int(opcode) == 4:
            parameters = get_parameters(tokens, current_index, 1)
            immediate_modes = list(immediate_modes)
            if len(immediate_modes) > 0 and int(immediate_modes[0]) == 1:
                output.append(parameters[0])
            else:
                output.append(tokens[parameters[0]])
            current_index += 2

        if int(opcode) == 5:
            parameters = get_parameters_and_resolve(tokens, current_index, 2)
            if not(int(parameters[0]) == 0):
                current_index = parameters[1]
            else:
                current_index += 3

        if int(opcode) == 6:
            parameters = get_parameters_and_resolve(tokens, current_index, 2)
            if int(parameters[0]) == 0:
                current_index = parameters[1]
            else:
                current_index += 3

        if int(opcode) == 7:
            parameters = get_parameters_and_resolve(tokens, current_index, 2)
            if int(parameters[0]) < int(parameters[1]):
                tokens[int(tokens[current_index+3])] = 1
            else:
                tokens[int(tokens[current_index+3])] = 0
            current_index += 4

        if int(opcode) == 8:
            parameters = get_parameters_and_resolve(tokens, current_index, 2)
            if int(parameters[0]) == int(parameters[1]):
                tokens[int(tokens[current_index+3])] = 1
            else:
                tokens[int(tokens[current_index+3])] = 0
            current_index += 4

        opcode, immediate_modes = split_instruction(str(tokens[current_index]))
        counter += 1
    return output

with open('Day 7/data.txt', 'r') as f:
    token_stream  = f.read()
    tokens = token_stream.split(',')
    program_settings_array = itertools.permutations('01234', 5)
    max_value = -1
    for program_settings in program_settings_array:
        previous_program_output = 0
        for amplifier_value in program_settings:
            previous_program_output = run_program(tokens.copy(), [int(amplifier_value), previous_program_output])[0]
            if max_value < int(previous_program_output):
                max_value = int(previous_program_output)
                best_program_output = program_settings
    print(max_value)
    print(best_program_output)