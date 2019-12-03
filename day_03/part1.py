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

    line_segments = []
    for move in moves:
        new_segment = (current_position, current_position + move)
        line_segments.append(new_segment)
        current_position = current_position + move

    return line_segments


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

    first_segments = get_all_segments(first_moves)
    second_segments = get_all_segments(second_moves)

    segment_pairs = product(first_segments, second_segments)

    distances = []
    for first_segment, second_segment in segment_pairs:
        intersects, point = check_intersection(first_segment, second_segment)
        if intersects:
            distance = int(np.sum(np.abs(point)))
            if distance == 0:
                continue
            distances.append(distance)

    print(np.min(distances))


if __name__ == '__main__':
    main()
