from itertools import product
import numpy as np

import warnings
warnings.filterwarnings('error')


def get_moves(wire):
    movement_vectors = {
        'U': np.array([0, 1]),
        'D': np.array([0, -1]),
        'R': np.array([1, 0]),
        'L': np.array([-1, 0]),
    }
    tokens = wire.split(',')
    movements = [
        movement_vectors[token[0]] * int(token[1:])
        for token in tokens
    ]

    return movements


def get_all_segments(moves):
    current_position = np.zeros(2).astype('int')

    number_of_steps = {}
    line_segments = []
    steps_taken = 0
    for move in moves:
        new_segment = (current_position, current_position + move)

        if tuple(current_position) not in number_of_steps.keys():
            number_of_steps[tuple(current_position)] = steps_taken
        else:
            steps_taken = number_of_steps[tuple(current_position)]

        line_segments.append(new_segment)
        current_position = current_position + move
        steps_taken = steps_taken + int(np.sum(np.abs(move)))

    return line_segments, number_of_steps


def check_intersection(first_segment, second_segment):
    p1, p2 = first_segment
    p3, p4 = second_segment

    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    try:
        ta = (y3 - y4)*(x1 - x3) + (x4 - x3)*(y1 - y3)
        ta /= (x4 - x3)*(y1 - y2) - (x1 - x2)*(y4 - y3)

        tb = (y1 - y2)*(x1 - x3) + (x2 - x1)*(y1 - y3)
        tb /= (x4 - x3)*(y1 - y2) - (x1 - x2)*(y4 - y3)
    except RuntimeWarning:
        return False, None

    if 0 <= ta <= 1 and 0 <= tb <= 1:
        intersection = p1 + ta * (p2 - p1)
        return True, intersection

    return False, None


def main():
    with open('input.txt') as fd:
        first_wire, second_wire = fd.read().splitlines()

    first_moves = get_moves(first_wire)
    second_moves = get_moves(second_wire)

    first_segments, first_steps = get_all_segments(first_moves)
    second_segments, second_steps = get_all_segments(second_moves)

    segment_pairs = product(first_segments, second_segments)

    distances = []
    for first_segment, second_segment in segment_pairs:
        intersects, point = check_intersection(first_segment, second_segment)
        if intersects:
            first_point_diff = np.abs(first_segment[0] - point).sum()
            second_point_diff = np.abs(second_segment[0] - point).sum()

            first_steps_value = first_steps[tuple(first_segment[0])]
            second_steps_value = second_steps[tuple(second_segment[0])]

            first_steps_total = first_steps_value + first_point_diff
            second_steps_total = second_steps_value + second_point_diff

            distance = int(first_steps_total + second_steps_total)
            if distance == 0:
                continue
            distances.append(distance)

    print(np.min(distances))


if __name__ == '__main__':
    main()
