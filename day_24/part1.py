from scipy.ndimage import generic_filter
from argparse import ArgumentParser
from itertools import count
import numpy as np
import os


def build_parser():
    parser = ArgumentParser()

    parser.add_argument(
        'input_filename',
        type=str
    )

    return parser


def invert_dict(dictionary):
    return dict(map(reversed, dictionary.items()))


class Grid():
    def __init__(self, input_string):
        self.array = self.array_from_input_string(input_string)

        # Need to keep track of what states we've been in.
        self.visited_states = {self.state_hash}

        # And how long we have evolved for.
        self.minutes_passed = 0

        # And if we have reached a cycle, when.
        self.cycle_minute = None

    def array_from_input_string(self, input_string):
        # Remove trailing newline / whitespace then split on lines.
        split_input = input_string.rstrip().split(os.linesep)

        # Map the character in each row to booleans.
        grid_as_lists = [
            list(map(self.character_transform, row_string))
            for row_string in split_input
        ]

        return np.array(grid_as_lists, dtype=np.bool)

    # Could do this a different way (using truth value of == '#'), but
    # this allows flexibility if I want to stop using bools.
    character_map = {'.': False, '#': True}
    inverse_character_map = invert_dict(character_map)

    def character_transform(self, character):
        return self.character_map[character]

    def inverse_character_transform(self, character):
        return self.inverse_character_map[character]

    def __str__(self):
        def row_function(row):
            return ''.join([
                self.inverse_character_transform(entry)
                for entry in row
            ])

        return os.linesep.join(map(row_function, self.array))

    __repr__ = __str__

    @property
    def state_hash(self):
        return hash(str(self))

    # Cross shaped structuring element for 4-neighbourhood and self.
    footprint = np.array(
        [
            [False, True, False],
            [True, True, True],
            [False, True, False]
        ]
    )

    @staticmethod
    def next_state(neighbourhood):
        # Center is 3rd cell is 'neighbourhood', the rest are real neighbours.
        center = neighbourhood[2]
        num_bugs = np.count_nonzero(neighbourhood)
        if center:
            # Since neighbourhood includes self we care about 2 bugs, ourselves
            # and a neighbour.
            return num_bugs == 2
        else:
            # The number here is just like the problem setting.
            return num_bugs == 1 or num_bugs == 2

    def step(self):
        # Run this function over all grid locations to get the next state.
        # Locations outside of the array are rightly treated as zero.
        self.array = generic_filter(
            self.array, function=self.next_state,
            footprint=self.footprint, mode='constant'
        )

        # Do bookkeeping about how long has elapsed, keep a record that we've
        # seen this state, and check if we're in a cycle. Could alternatively
        # use a Counter on the hashes and check the max value to find the
        # cycle.
        self.minutes_passed += 1

        if self.state_hash in self.visited_states:
            self.cycle_minute = self.minutes_passed
        else:
            self.visited_states.add(self.state_hash)

    @property
    def has_cycle(self):
        return bool(self.cycle_minute)

    @property
    def biodiversity(self):
        # Create the appropriate weight array (all powers of two up to grid
        # size), multiply by it and sum up.
        grid_shape = self.array.shape
        exponents = np.arange(self.array.size).reshape(grid_shape)

        cell_coefficients = np.power(2, exponents)

        return np.sum(self.array * cell_coefficients)


def run_evolution(grid, quiet=False):
    if not quiet:
        print('Initial state:')
        print(grid)
        print()

    def iterate():
        grid.step()

        if not quiet:
            suffix = 's' if minute > 1 else ''
            print(f'After {minute} minute{suffix}')
            print(grid)
            print()

    for minute in count(1):
        iterate()

        if grid.has_cycle:
            return


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        input_string = fd.read()

    grid = Grid(input_string)

    run_evolution(grid, quiet=False)

    print(f'Cycle at minute {grid.cycle_minute}')
    print(f'Biodiversity is {grid.biodiversity}')


if __name__ == '__main__':
    main()
