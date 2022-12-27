from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def move(
    current_pos: tuple[int, int],
    nb_step: int,
    direction: support.Direction4,
    board: dict[tuple[int, int], str],
) -> tuple[int, int]:
    for _ in range(nb_step):
        next_pos = direction.apply(*current_pos)
        if next_pos not in board:  # overflow, need to wrap
            if direction is support.Direction4.UP:
                next_pos = (
                    current_pos[0],
                    max(y for (x, y) in board if x == current_pos[0]),
                )
            elif direction is support.Direction4.DOWN:
                next_pos = (
                    current_pos[0],
                    min(y for (x, y) in board if x == current_pos[0]),
                )
            if direction is support.Direction4.RIGHT:
                next_pos = (
                    min(x for (x, y) in board if y == current_pos[1]),
                    current_pos[1],
                )
            elif direction is support.Direction4.LEFT:
                next_pos = (
                    max(x for (x, y) in board if y == current_pos[1]),
                    current_pos[1],
                )

        if board[next_pos] == "#":  # Stop moving and stay at previous pos
            break

        current_pos = next_pos

    return current_pos


def compute(s: str) -> int:
    print("\n")
    board_s, instructions = s.split("\n\n")

    board = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c in ".#":
                board[(x, y)] = c

    current_dir = support.Direction4.RIGHT
    current_digit = ""
    current_pos = (min(x for (x, y) in board if y == 0), 0)
    for instruction in instructions.strip():
        if instruction.isdigit():
            current_digit += instruction
        else:
            # Process move forward instruction
            nb_step = int(current_digit)
            current_pos = move(current_pos, nb_step, current_dir, board)
            # Process rotate instruction and reset current
            current_digit = ""
            if instruction == "R":
                current_dir = current_dir.cw
            elif instruction == "L":
                current_dir = current_dir.ccw
            else:
                raise AssertionError(f"Drunk instruction here {instruction!r}")

    facing_pts = {
        support.Direction4.RIGHT: 0,
        support.Direction4.DOWN: 1,
        support.Direction4.LEFT: 2,
        support.Direction4.UP: 3,
    }

    return (
        1000 * (current_pos[1] + 1) + 4 * (current_pos[0] + 1) + facing_pts[current_dir]
    )


INPUT_S = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""
EXPECTED = 6032


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
