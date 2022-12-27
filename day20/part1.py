from __future__ import annotations

import argparse
import os.path
from collections import deque
from unittest import mock

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    print("\n")

    numbers: list[tuple[int, int]] = list(enumerate(map(int, s.splitlines())))
    deck = deque(numbers)  # Enumerate to prevent duplicate.
    for i, n in numbers:
        move(deck, (i, n))

    zero_idx = deck.index((mock.ANY, 0))

    return sum(deck[(zero_idx + i * 1000) % len(deck)][1] for i in range(1, 4))


def move(deck: deque, n: tuple[int, int]) -> None:
    pos = deck.index(n)  # Get current number position in deck

    deck.rotate(-pos)  # Move number to the left side
    deck.popleft()  # Pop number from the side
    deck.rotate(-n[1])  # Do the inverted rotation to insert the number
    deck.appendleft(n)  # Insert the number
    deck.rotate(n[1])  # Do the actual rotation


INPUT_S = """\
1
2
-3
3
-2
0
4
"""
EXPECTED = 3


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
