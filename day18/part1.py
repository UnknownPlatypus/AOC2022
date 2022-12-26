from __future__ import annotations

import argparse
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


def compute(s: str) -> int:
    print("\n")
    tot = 0

    seen = set()
    for line in s.splitlines():
        x, y, z = map(int, line.split(","))
        seen.add((x, y, z))
        tot += 6

        for ax, ay, az in adjacent_points(x, y, z):
            if (ax, ay, az) in seen:
                # They are adjacent so they share 1 side.
                tot -= 2

    return tot


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
EXPECTED = 64


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
