from __future__ import annotations

import argparse
import collections
import os.path
from typing import Iterable, Tuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

State = Tuple[
    int,
    int,
    int,
    Tuple[int, ...],
    Tuple[int, ...],
    Tuple[int, ...],
    Tuple[int, ...],
]


def find_path(
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    up: tuple[int, ...],
    down: tuple[int, ...],
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    seen = set()
    depth = 0
    todo = collections.deque([(depth, start_x, start_y, up, down, left, right)])
    width = len(left)
    height = len(up)

    while todo:
        state: State = todo.popleft()
        depth, x, y, up, down, left, right = state
        new_depth = depth + 1

        # print(depth, x, y)
        if y not in {-1, height} and (
            (1 << x) & (up[y] | down[y]) or (1 << y) & (left[x] | right[x])
        ):
            # Impossible state, current position is in the blizzard.
            continue
        elif x == end_x and y == end_y:
            # Final position reached
            return new_depth, up, down, left, right

        if state in seen:
            continue
        else:
            seen.add(state)

        next_up = (*up[1:], up[0])
        next_down = (down[-1], *down[:-1])
        next_left = (*left[1:], left[0])
        next_right = (right[-1], *right[:-1])

        # Do nothing
        todo.append((new_depth, x, y, next_up, next_down, next_left, next_right))

        # Move in all 4 possible directions
        for (next_x, next_y) in support.adjacent_4(x, y):
            if 0 <= next_x < width and 0 <= next_y < height:
                todo.append(
                    (
                        new_depth,
                        next_x,
                        next_y,
                        next_up,
                        next_down,
                        next_left,
                        next_right,
                    ),
                )
    raise AssertionError("unreachable!")


def compute(s: str) -> int:
    lines = [line[1:-1] for line in s.splitlines()[1:-1]]
    width = len(lines[0])
    height = len(lines)

    joined_s = "".join(lines)
    columns = [joined_s[i::width] for i in range(width)]

    start_x, start_y = 0, -1
    end_x, end_y = width - 1, height - 1

    # Compute bitmask for every wind direction.
    # Will be useful later to simulate wind movement with a bitshift.
    up = tuple(
        int("".join("1" if s == "^" else "0" for s in line)[::-1], 2) for line in lines
    )
    down = tuple(
        int("".join("1" if s == "v" else "0" for s in line)[::-1], 2) for line in lines
    )
    left = tuple(
        int("".join("1" if s == "<" else "0" for s in c)[::-1], 2) for c in columns
    )
    right = tuple(
        int("".join("1" if s == ">" else "0" for s in c)[::-1], 2) for c in columns
    )
    # print(up, down, left, right, sep="\n")

    # Do the traversal 3 times.
    dirs: Iterable[tuple[int, ...]] = up, down, left, right
    tot1, *dirs = find_path(start_x, start_y, end_x, end_y, *dirs)
    print("1 ->", tot1)

    tot2, up, down, left, right = find_path(
        end_x,
        end_y + 1,
        start_x,
        start_y + 1,
        *dirs,
    )
    print("2 ->", tot2)

    tot3, *_ = find_path(start_x, start_y, end_x, end_y, *dirs)
    print("3 ->", tot3)

    return tot1 + tot2 + tot3 - 2


INPUT_S = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""
EXPECTED = 54


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
