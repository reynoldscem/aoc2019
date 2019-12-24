from itertools import product
from copy import deepcopy


def process_program(program, input_1, input_2):
    program = deepcopy(program)
    program[1] = input_1
    program[2] = input_2
    # print(program)
    program_counter = 0
    while True:
        opcode = program[program_counter]
        # print(opcode)

        if opcode == 1:
            operand_a = program[program[program_counter + 1]]
            operand_b = program[program[program_counter + 2]]
            destination = program[program_counter + 3]
            # print(f'Add {operand_a} and {operand_b} save to {destination}')
            program[destination] = operand_a + operand_b
        elif opcode == 2:
            operand_a = program[program[program_counter + 1]]
            operand_b = program[program[program_counter + 2]]
            destination = program[program_counter + 3]
            # print(f'Mul {operand_a} and {operand_b} save to {destination}')
            program[destination] = operand_a * operand_b
        elif opcode == 99:
            break
        else:
            raise ValueError(f'Invalid opcode encountered: {opcode}')

        program_counter += 4

    return program[0]


def main():
    target = 19690720

    with open('input.txt') as fd:
        lines = fd.read().split(',')
    program = [int(entry) for entry in lines]

    input_pairs = product(range(100), range(100))
    for input_1, input_2 in input_pairs:
        result = process_program(program, input_1, input_2)
        if result == target:
            print(input_1, input_2)
            break


if __name__ == '__main__':
    main()
