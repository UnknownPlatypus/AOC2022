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


def move_current_tail(head: Point, tail: Point) -> Point:
    if abs(head.x - tail.x) > 1 and abs(head.y - tail.y) > 1:
        return Point((head.x + tail.x) // 2, (head.y + tail.y) // 2)
    if abs(head.x - tail.x) > 1:
        return Point((head.x + tail.x) // 2, head.y)
    elif abs(head.y - tail.y) > 1:
        return Point(head.x, (head.y + tail.y) // 2)
    return tail


def compute(s: str) -> int | None:
    positions = [
        Point(0, 0) for _ in range(10)
    ]  # head is positions[0], tail is positions[-1]
    visited = {positions[0]}

    for instruction in s.splitlines():
        direction, amount_s = instruction.split()
        amount = int(amount_s)
        move = MOVES[direction]

        for _ in range(amount):
            positions[0] += move  # Move head first.

            for i in range(1, len(positions)):
                positions[i] = move_current_tail(positions[i - 1], positions[i])

            visited.add(positions[-1])  # tail
    return len(visited)


INPUT_S = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
EXPECTED = 36


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
