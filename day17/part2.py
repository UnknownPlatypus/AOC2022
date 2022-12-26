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


def max_heights(places: set[tuple[int, int]]) -> list[int]:
    m = [0] * 7
    for x, y in places:
        m[x] = max(y, m[x])
    return m


def compute_max_from_cycle(
    seen: dict[tuple[int, ...], tuple[int, int]],
    current_state: tuple[int, ...],
    i: int,
    max_height: int,
) -> int:
    """We found a cycle when adding rocks.

    The total height will be the sum of:
        - the max_height at the start of the cycle.
        - the cycle height times (1_000_000_000_000 - start_i) // cycle_len.
        - the leftover height for the few remaining iteration.
          (we can infer that from the saved state in seen)
    """
    start_i, start_max_height = seen[current_state]
    cycle_len = i - start_i
    cycle_height = max_height - start_max_height

    nb_iter_remaining = 1_000_000_000_000 - start_i
    nb_cycle_iter = nb_iter_remaining // cycle_len

    leftover = nb_iter_remaining % cycle_len
    leftover_height = (
        next(height for i, height in seen.values() if i == leftover + start_i - 1)
        - start_max_height
    )
    return start_max_height + nb_cycle_iter * cycle_height + leftover_height


def move(
    stale: set[tuple[int, int]],
    shape: Shape,
    x: int,
    y: int,
    direction: Literal["<", ">"],
) -> int:
    if direction == "<" and x != 0 and not shape.at(x - 1, y) & stale:
        return x - 1
    if direction == ">" and x + shape.width != 7 and not shape.at(x + 1, y) & stale:
        return x + 1
    return x


def compute(s: str) -> int:
    print("\n")

    shapes = itertools.cycle(
        enumerate(
            Shape(support.parse_coords_hash(shape_hash))
            for shape_hash in SHAPES.split("\n\n")
        ),
    )

    winds: itertools.cycle[tuple[int, Literal["<", ">"]]] = itertools.cycle(enumerate(s.strip()))  # type: ignore
    stale = support.parse_coords_hash("#######")

    max_height = 0
    top_heights = [0] * 7
    seen: dict[tuple[int, ...], tuple[int, int]] = {}

    for i in range(20000):
        shape_id, shape = next(shapes)
        # Each rock appears so that its left edge is two units away from the left wall
        x = 2
        # and its bottom edge is three units above the highest rock in the room.
        y = 3 + max_height + shape.height

        # Move shape until stale
        while True:
            wind_id, wind = next(winds)
            x = move(stale, shape, x, y, wind)

            if shape.at(x, y - 1) & stale:
                new_stale_shape = shape.at(x, y)
                stale |= new_stale_shape

                # Find max height for every column with this new stale shape.
                shape_max_heights = max_heights(new_stale_shape)
                for x in range(7):
                    top_heights[x] = max(top_heights[x], shape_max_heights[x])
                max_height = max(top_heights)

                # Create a normalized state.
                current_state = (
                    shape_id,
                    wind_id,
                    *(h - max_height for h in top_heights),
                )
                if current_state in seen:
                    return compute_max_from_cycle(seen, current_state, i, max_height)
                seen[current_state] = (i, max_height)
                break
            else:
                y -= 1

    return max_height


INPUT_S = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""
EXPECTED = 1514285714288


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
