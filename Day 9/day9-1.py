import sys
import itertools
class Program:
    def __init__(self, tokens, phase_setting):
        self.tokens = tokens
        self.current_index = 0
        self.relative_reference_index = 0
        self.run_step(phase_setting)

    def run_until_output(self, input_value):
        input_consumed_times = 0
        done, output, input_consumed = self.run_step(input_value)
        if input_consumed:
            input_consumed_times += 1
        while not done and len(output) == 0:
            done, output, input_consumed = self.run_step(input_value)
            if input_consumed:
                input_consumed_times += 1
        if input_consumed_times > 1:
            print("never supposed to happen")
        return output

    def run_step(self, input_value):
        output = []
        input_consumed = False
        opcode, immediate_modes = split_instruction(str(self.tokens[self.current_index]))
        if opcode == 99:
            return True, [], False
        if opcode == 1:
            parameters = self.get_parameters_and_resolve(2)
            self.assign_with_immediate(parameters[0] + parameters[1], immediate_modes, 3)
            self.current_index += 4

        if opcode == 2:
            parameters = self.get_parameters_and_resolve(2)
            self.assign_with_immediate(parameters[0] * parameters[1], immediate_modes, 3)
            self.current_index += 4

        if opcode == 3:
            # print('something', input_value, immediate_modes, 1)
            self.assign_with_immediate(input_value, immediate_modes, 1)
            input_consumed = True
            self.current_index += 2

        if opcode == 4:
            parameters = self.get_parameters_and_resolve(1)
            print('output:', parameters[0])
            output.append(parameters[0])
            self.current_index += 2

        if opcode == 5:
            parameters = self.get_parameters_and_resolve(2)
            if not(parameters[0] == 0):
                self.current_index = parameters[1]
            else:
                self.current_index += 3

        if opcode == 6:
            parameters = self.get_parameters_and_resolve(2)
            if parameters[0] == 0:
                self.current_index = parameters[1]
            else:
                self.current_index += 3

        if opcode == 7:
            parameters = self.get_parameters_and_resolve(2)
            rhs = -1
            if parameters[0] < parameters[1]:
                rhs = 1
            else:
                rhs = 0
            self.assign_with_immediate(rhs, immediate_modes, 3)
            self.current_index += 4

        if opcode == 8:
            parameters = self.get_parameters_and_resolve(2)
            rhs = -1
            if parameters[0] == parameters[1]:
                rhs = 1
            else:
                rhs = 0
            self.assign_with_immediate(rhs, immediate_modes, 3)
            self.current_index += 4

        if opcode == 9:
            parameters = self.get_parameters_and_resolve(1)
            self.relative_reference_index += parameters[0]
            # print('relative_reference_index=', self.relative_reference_index)
            self.current_index += 2

        return False, output, input_consumed

    def assign_with_immediate(self, rhs, immediate_modes, current_index_relative):
        immediate_modes = list(str(immediate_modes))
        immediate_modes.reverse()
        immediate_mode = get_immediate_mode_or_default(current_index_relative - 1, immediate_modes)
        # print('assigning', immediate_mode, 'from', immediate_modes, 'and', current_index_relative)
        if immediate_mode == 0:
            final_assignment_position = self.tokens[self.current_index + current_index_relative]
        elif immediate_mode == 2:
            final_assignment_position = self.tokens[self.current_index + current_index_relative] + self.relative_reference_index
        else:
            print('bad stuff happened, immediate mode not 0 or 2 for assignment', immediate_mode, self.current_index, self.tokens[self.current_index])
        self.tokens[final_assignment_position] = int(rhs)

    def resolve_parameters(self, immediate_modes, parameters):
        immediate_modes = list(str(immediate_modes))
        immediate_modes.reverse()
        # print('immediate', immediate_modes)
        for i in range(len(parameters)):
            immediate_mode =int(immediate_modes[i])

            if i >= len(immediate_modes) or immediate_mode == 0: # position mode
                parameters[i] = self.tokens.get(parameters[i], 0)
            elif immediate_mode == 2: # relative reference mode
                parameters[i] = self.tokens.get(self.relative_reference_index + parameters[i], 0)
            # print()
        return parameters

    def get_parameters_and_resolve(self, num_parameters):
        opcode, immediate_modes = split_instruction(str(self.tokens[self.current_index]))
        return [int(x) for x in self.resolve_parameters(immediate_modes, get_parameters(self.tokens, self.current_index, num_parameters))]

def get_immediate_mode_or_default(index, immediate_modes):
    if index <= len(immediate_modes) - 1 and index >= 0:
        return int(immediate_modes[index])
    return 0
def yellow(text):
    return '\033[33m' + text + '\033[0m'
def get_slice(tokens, from_index, to_index):
    token_slice = []
    for i in range(from_index, to_index):
        token_slice.append(tokens[i])
    return token_slice

def get_parameters(tokens, current_index, num_parameters):
    return [int(x) for x in get_slice(tokens, current_index + 1, current_index + 1 + num_parameters)]

def split_instruction(token):
    return int(token[-2:]), int(token[:-2] or 0)

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
    amp = Program(tokens, input_array[0])
    output = amp.run_until_output(input_array[1])
    print(output)
    return output

with open('Day 9/data.txt', 'r') as f:
    token_stream  = f.read()
    tokens = token_stream.split(',')
    tokens_dict = { i : int(tokens[i]) for i in range(len(tokens)) }
    prgm = Program(tokens_dict.copy(), 2)
    output = []
    current_output = prgm.run_until_output(2)
    print('current_output', current_output)
    while len(current_output) > 0:
        output.append(current_output[0])
        current_output = prgm.run_until_output(2)
    print(output)
    # program_settings_array = itertools.permutations('56789', 5)
    # max_value = -1
    # for program_settings in program_settings_array:
    #     previous_program_output = 0
    #     programs = []
    #     for amplifier_value in program_settings:
    #         programs.append(Program(tokens_dict.copy(), int(amplifier_value)))
    #     output = programs[0].run_until_output(0)
    #     counter = 1
    #     final_output = -1
    #     while len(output) > 0:
    #         output = programs[counter].run_until_output(output[0])
    #         counter += 1
    #         if counter >= len(programs):
    #             if len(output) > 0:
    #                 final_output = int(output[0])
    #             counter = 0
    #     if max_value < final_output:
    #         max_value = int(final_output)
    #         best_program_output = program_settings
    # print(max_value)
    # print(best_program_output)