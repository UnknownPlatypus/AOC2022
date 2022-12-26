from __future__ import annotations

import argparse
import itertools
import os.path
from typing import Iterator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def adjacent_points(x: int, y: int, z: int) -> Iterator[tuple[int, int, int]]:
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1


def surface_total(points: set[tuple[int, int, int]]) -> int:
    tot = 0
    seen = set()
    for x, y, z in points:
        seen.add((x, y, z))
        tot += 6

        for point in adjacent_points(x, y, z):
            if point in seen:
                # They are adjacent so they share 1 side.
                tot -= 2
    return tot


def compute(s: str) -> int:
    print("\n")

    points: set[tuple[int, int, int]] = {
        tuple(map(int, line.split(","))) for line in s.splitlines()  # type:ignore[misc]
    }
    tot = surface_total(points)

    # Compute min-max accross every axis.
    x_vals = [x for x, _, _ in points]
    y_vals = [y for y, _, _ in points]
    z_vals = [z for z, _, _ in points]

    min_x, max_x = min(x_vals), max(x_vals)
    min_y, max_y = min(y_vals), max(y_vals)
    min_z, max_z = min(z_vals), max(z_vals)

    # For non lava blocks, check if they are trapped.
    remaining = (
        set(
            itertools.product(
                range(min_x, max_x + 1),
                range(min_y, max_y + 1),
                range(min_z, max_z + 1),
            ),
        )
        - points
    )

    todo = [min(remaining)]
    while todo:
        point = todo.pop()
        if point in remaining:
            remaining.discard(point)
        else:
            continue

        todo.extend(iter(adjacent_points(*point)))

    # Get total area trapped block
    trapped_tot = surface_total(remaining)
    return tot - trapped_tot


def surface_area(pts: set[tuple[int, int, int]]) -> int:
    count = 0
    coords = set()

    for pt in pts:
        count += 6
        for cpt in adjacent_points(*pt):
            if cpt in coords:
                count -= 2
        coords.add(pt)
    return count


INPUT_S = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""
EXPECTED = 58


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
