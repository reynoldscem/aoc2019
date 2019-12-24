from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()

    parser.add_argument(
        'input_filename',
        type=str
    )

    return parser


def valid_password(password):
    digits = list(map(int, str(password)))

    consecutive = False
    for first, second in zip(digits[:-1], digits[1:]):
        if second < first:
            return False

        if first == second:
            consecutive = True
    if not consecutive:
        return False

    return True


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        input_string = fd.read()
        lower, upper = map(int, input_string.split('-'))

    valid_count = 0
    for password in range(lower, upper + 1):
        if valid_password(password):
            valid_count += 1
    print(valid_count)


if __name__ == '__main__':
    main()
