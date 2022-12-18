from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def min_max_range(x: int, y: int) -> range:
    return range(y, x + 1) if x > y else range(x, y + 1)


def compute(s: str) -> int:
    cells: set[tuple[int, int]] = set()

    # Track every celles initially filled with rock.
    for line in s.splitlines():
        points = line.split(" -> ")
        x, y = support.parse_point_comma(points[0])
        for next_point in points[1:]:
            next_x, next_y = support.parse_point_comma(next_point)
            if x == next_x:
                cells.update((next_x, y) for y in min_max_range(y, next_y))
            else:
                cells.update((x, next_y) for x in min_max_range(x, next_x))
            x, y = next_x, next_y

    bedrock_y = max(y for _, y in cells)

    # Emulate Sand falling. Stop when bedrock_y is reached.
    tot = 0
    while True:
        x, y = 500, 0
        # test move bot, else move left else move right.
        while True:  # Process one sand chunk
            if (x, y) in cells:
                return tot
            elif y == bedrock_y + 1:  # sand overflow
                cells.add((x, y))
                break
            if (x, y + 1) not in cells:  # move down OK
                y += 1
            elif (x - 1, y + 1) not in cells:  # move left down
                x -= 1
                y += 1
            elif (x + 1, y + 1) not in cells:  # move right down
                x += 1
                y += 1
            else:  # Sand rest
                cells.add((x, y))
                break

        tot += 1


INPUT_S = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
EXPECTED = 93


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
