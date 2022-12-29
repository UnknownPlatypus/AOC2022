from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    print("\n")
    moves = collections.deque(
        [
            (((0, -1), (-1, -1), (1, -1)), support.Direction4.UP),
            (((0, 1), (-1, 1), (1, 1)), support.Direction4.DOWN),
            (((-1, 0), (-1, 1), (-1, -1)), support.Direction4.LEFT),
            (((1, 0), (1, 1), (1, -1)), support.Direction4.RIGHT),
        ],
    )

    board = support.parse_coords_hash(s)
    for _ in range(10):
        next_move = collections.defaultdict(list)
        for x, y in board:
            if all(  # No one around, don't move.
                (dx, dy) not in board for dx, dy in support.adjacent_8(x, y)
            ):
                continue
            for next_points, direction in moves:
                if all((x + dx, y + dy) not in board for (dx, dy) in next_points):
                    next_move[direction.apply(x, y)].append((x, y))
                    break

        eligible_moves = {k: v[0] for k, v in next_move.items() if len(v) == 1}
        board = (board - set(eligible_moves.values())) | set(eligible_moves.keys())

        moves.rotate(-1)

        # print("-------------------------")
        # support.print_coords_hash(board)

    # Get Bounds
    x_vals = [x for (x, _) in board]
    y_vals = [y for (_, y) in board]
    size_x = max(x_vals) - min(x_vals) + 1
    size_y = max(y_vals) - min(y_vals) + 1
    return (size_x * size_y) - len(board)


INPUT_S = """\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""
EXPECTED = 110


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
