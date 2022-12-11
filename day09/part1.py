from __future__ import annotations

import argparse
import os.path
from dataclasses import dataclass

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    @property
    def opposite(self) -> Point:
        return Point(-self.x, -self.y)


MOVES = {
    "U": Point(0, 1),
    "D": Point(0, -1),
    "L": Point(-1, 0),
    "R": Point(1, 0),
}


def compute(s: str) -> int | None:
    head = tail = Point(0, 0)
    visited = {tail}
    for instruction in s.splitlines():
        direction, amount_s = instruction.split()
        amount = int(amount_s)
        move = MOVES[direction]
        for _ in range(amount):
            head += move
            if abs(head.x - tail.x) >= 2 or abs(head.y - tail.y) >= 2:
                tail = head + move.opposite  # Go the last head position
                visited.add(tail)
    return len(visited)


INPUT_S = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
EXPECTED = 13


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

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
