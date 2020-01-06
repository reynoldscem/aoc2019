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
        grid_as_lists = [
            list(map(self.character_transform, row_string))
            for row_string in input_string.rstrip().split(os.linesep)
        ]

        return np.array(grid_as_lists, dtype=np.bool)

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
        center = neighbourhood[2]
        num_bugs = np.count_nonzero(neighbourhood)
        if center:
            return num_bugs == 2
        else:
            return num_bugs == 1 or num_bugs == 2

    def step(self):
        self.array = generic_filter(
            self.array, function=self.next_state,
            footprint=self.footprint, mode='constant'
        )
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
        grid_shape = self.array.shape
        exponents = np.arange(self.array.size).reshape(grid_shape)

        cell_coefficients = np.power(2, exponents)

        return np.sum(self.array * cell_coefficients)


def run_evolution(grid):
    print('Initial state:')
    print(grid)
    print()

    for minute in count(1):
        grid.step()
        print(f'After {minute} minute(s)')
        print(grid)
        print()

        if grid.has_cycle:
            print(f'Cycle at minute {grid.cycle_minute}')
            print(f'Biodiversity is {grid.biodiversity}')
            break


def main():
    args = build_parser().parse_args()

    with open(args.input_filename) as fd:
        input_string = fd.read()

    grid = Grid(input_string)

    run_evolution(grid)


if __name__ == '__main__':
    main()
