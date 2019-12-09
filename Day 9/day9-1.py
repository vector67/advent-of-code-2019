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
        if int(opcode) == 99:
            return True, [], False
        if int(opcode) == 1:
            parameters = self.get_parameters_and_resolve(2)
            self.tokens[int(self.tokens[self.current_index+3])] = str(parameters[0] + parameters[1])
            self.current_index += 4

        if int(opcode) == 2:
            parameters = self.get_parameters_and_resolve(2)
            self.tokens[int(self.tokens[self.current_index+3])] = str(parameters[0] * parameters[1])
            self.current_index += 4

        if int(opcode) == 3:
            parameters = self.get_parameters(self.tokens, self.current_index, 1)
            self.tokens[parameters[0]] = input_value
            input_consumed = True
            self.current_index += 2

        if int(opcode) == 4:
            parameters = self.get_parameters_and_resolve(1)
            output.append(parameters[0])
            self.current_index += 2

        if int(opcode) == 5:
            parameters = self.get_parameters_and_resolve(2)
            if not(int(parameters[0]) == 0):
                self.current_index = parameters[1]
            else:
                self.current_index += 3

        if int(opcode) == 6:
            parameters = self.get_parameters_and_resolve(2)
            if int(parameters[0]) == 0:
                self.current_index = parameters[1]
            else:
                self.current_index += 3

        if int(opcode) == 7:
            parameters = self.get_parameters_and_resolve(2)

            if int(parameters[0]) < int(parameters[1]):
                self.tokens[int(self.tokens[self.current_index+3])] = 1
            else:
                self.tokens[int(self.tokens[self.current_index+3])] = 0
            self.current_index += 4

        if int(opcode) == 8:
            parameters = self.get_parameters_and_resolve(2)
            immediate_mode = get_immediate_mode_or_default(0, immediate_modes)
            if int(parameters[0]) == int(parameters[1]):
                self.assign_with_immediate(self.current_index+3, 1, immediate_mode)
            else:
                self.tokens[int(self.tokens[self.current_index+3])] = 0
            self.current_index += 4
        return False, output, input_consumed

    def assign_with_immediate(self, lhs, rhs, immediate_mode):
        if immediate_mode == 0:
            self.tokens[self.tokens[lhs]] = rhs
        elif immediate_mode == 2:
            self.tokens[lhs + self.relative_reference_index] = rhs
        else:
            print('bad stuff happened, immediate mode not 0 or 2 for assignment')

    def resolve_parameters(self, immediate_modes, parameters):
        immediate_modes = list(immediate_modes)
        immediate_modes.reverse()
        # print('immediate', immediate_modes)
        for i in range(len(parameters)):
            immediate_mode = int(immediate_modes[i])

            if i >= len(immediate_modes) or immediate_mode == 0: # position mode
                parameters[i] = self.tokens[int(parameters[i])]
            elif immediate_mode == 2: # relative reference mode
                parameters[i] = self.tokens[self.relative_reference_index]
            # print()
    return parameters

    def get_parameters_and_resolve(self, num_parameters):
        opcode, immediate_modes = split_instruction(self.tokens[self.current_index])
        return [int(x) for x in self.resolve_parameters(self.tokens, immediate_modes, get_parameters(self.tokens, self.current_index, num_parameters))]

def get_immediate_mode_or_default(index, immediate_modes):
    if len(immediate_modes) >= index:
        return immediate_modes[index]
    return 0
def yellow(text):
    return '\033[33m' + text + '\033[0m'

def get_parameters(tokens, current_index, num_parameters):
    return [int(x) for x in tokens[current_index + 1: current_index + 1 + num_parameters]]

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
    amp = Program(tokens, input_array[0])
    output = amp.run_until_output(input_array[1])
    print(output)
    return output

with open('Day 9/data.txt', 'r') as f:
    token_stream  = f.read()
    tokens = token_stream.split(',')
    tokens_dict = { i : tokens[i] for i in range(len(tokens)) }
    program_settings_array = itertools.permutations('56789', 5)
    max_value = -1
    for program_settings in program_settings_array:
        previous_program_output = 0
        programs = []
        for amplifier_value in program_settings:
            programs.append(Program(tokens_dict.copy(), int(amplifier_value)))
        output = programs[0].run_until_output(0)
        counter = 1
        final_output = -1
        while len(output) > 0:
            output = programs[counter].run_until_output(output[0])
            counter += 1
            if counter >= len(programs):
                if len(output) > 0:
                    final_output = int(output[0])
                counter = 0
        if max_value < final_output:
            max_value = int(final_output)
            best_program_output = program_settings
    print(max_value)
    print(best_program_output)