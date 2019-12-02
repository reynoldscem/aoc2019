def main():
    with open('input.txt') as fd:
        lines = fd.read().splitlines()
    total = 0
    for line in lines:
        fuel_for_mass = (int(line) // 3) - 2
        total += fuel_for_mass
    print(total)


if __name__ == '__main__':
    main()
