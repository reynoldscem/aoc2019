def main():
    with open('input.txt') as fd:
        lines = fd.read().splitlines()
    total = 0
    for line in lines:
        fuel_for_mass = int(line)
        while True:
            fuel_for_mass = (fuel_for_mass // 3) - 2
            if fuel_for_mass <= 0:
                break
            total += fuel_for_mass
    print(total)


if __name__ == '__main__':
    main()
