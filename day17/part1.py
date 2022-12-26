from __future__ import annotations

import argparse
import functools
import itertools
import os.path
from typing import Literal

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

SHAPES = """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""


class Shape:
    def __init__(self, places: set[tuple[int, int]]) -> None:
        self.places = {(x, -y) for x, y in places}

    @functools.cached_property
    def width(self) -> int:
        x_vals = [x for x, _ in self.places]
        return max(x_vals) - min(x_vals) + 1

    @functools.cached_property
    def height(self) -> int:
        y_vals = [y for _, y in self.places]
        return max(y_vals) - min(y_vals) + 1

    def at(self, dx: int, dy: int) -> set[tuple[int, int]]:
        return {(x + dx, y + dy) for x, y in self.places}

    def __str__(self) -> str:
        return (
            f"Shape(width={self.width}, height={self.height}, places={self.places}, "
            f"hash=\n----\n{support.format_coords_hash(self.places, -1)}\n----\n)"
        )


DIR = Literal["<", ">"]


def move(
    stale: set[tuple[int, int]],
    shape: Shape,
    x: int,
    y: int,
    direction: DIR,
) -> int:
    if direction == "<" and x != 0 and not shape.at(x - 1, y) & stale:
        return x - 1
    if direction == ">" and x + shape.width != 7 and not shape.at(x + 1, y) & stale:
        return x + 1
    return x


def compute(s: str) -> int:
    print("\n")

    shapes = itertools.cycle(
        Shape(support.parse_coords_hash(shape_hash))
        for shape_hash in SHAPES.split("\n\n")
    )

    wind: itertools.cycle[DIR] = itertools.cycle(s.strip())  # type: ignore
    stale = support.parse_coords_hash("#######")
    max_height = 0

    for _ in range(2022):
        shape = next(shapes)
        # Each rock appears so that its left edge is two units away from the left wall
        x = 2
        # and its bottom edge is three units above the highest rock in the room.
        y = 3 + max_height + shape.height

        # Move shape until stale
        while True:
            x = move(stale, shape, x, y, next(wind))

            if shape.at(x, y - 1) & stale:
                stale |= shape.at(x, y)
                max_height = max(max_height, y)
                break
            else:
                y -= 1
        # print(_, shape)
        # support.print_coords_hash(stale, -1)

    return max_height


INPUT_S = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""
EXPECTED = 3068


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
