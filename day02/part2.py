from __future__ import annotations

import argparse
import os.path
from collections import Counter

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

points = {"A": 1, "B": 2, "C": 3}
win = {"C": "B", "B": "A", "A": "C"}
lose = {"C": "A", "B": "C", "A": "B"}


def compute(s: str) -> int:
    c = Counter(s.splitlines())
    total = 0

    for comb, nb in c.items():
        x, y = comb.split()
        if y == "X":  # LOSS
            y = win[x]
        elif y == "Z":  # WIN
            y = lose[x]
        else:  # TIE
            y = x

        if x == y:
            total += 3 * nb
        elif win[y] == x:
            total += 6 * nb

        total += points[y] * nb

    return total


INPUT_S = """\
A Y
B X
C Z
"""
EXPECTED = 12


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
