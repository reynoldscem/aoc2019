def main():
    with open('input.txt') as fd:
        lines = fd.read().split(',')
    program = [int(entry) for entry in lines]
    program[1] = 12
    program[2] = 2
    print(program)
    program_counter = 0
    while True:
        opcode = program[program_counter]
        print(opcode)

        if opcode == 1:
            operand_a = program[program[program_counter + 1]]
            operand_b = program[program[program_counter + 2]]
            destination = program[program_counter + 3]
            print(f'Add {operand_a} and {operand_b} save to {destination}')
            program[destination] = operand_a + operand_b
        elif opcode == 2:
            operand_a = program[program[program_counter + 1]]
            operand_b = program[program[program_counter + 2]]
            destination = program[program_counter + 3]
            print(f'Mul {operand_a} and {operand_b} save to {destination}')
            program[destination] = operand_a * operand_b
        elif opcode == 99:
            break
        else:
            raise ValueError(f'Invalid opcode encountered: {opcode}')

        program_counter += 4

    print(program)
    print(program[0])


if __name__ == '__main__':
    main()
