from __future__ import annotations

import argparse
import os.path
from collections import Counter

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

points = {"A": 1, "B": 2, "C": 3}
win = {"C": "B", "B": "A", "A": "C"}


def compute(s: str) -> int:
    c = Counter(s.splitlines())
    total = 0

    for comb, nb in c.items():
        comb = comb.replace("X", "A").replace("Y", "B").replace("Z", "C")
        x, y = comb.split()
        if x == y:  # TIE
            total += 3 * nb
        elif win[y] == x:  # WIN
            total += 6 * nb

        total += points[y] * nb
    return total


INPUT_S = """\
A Y
B X
C Z
"""
EXPECTED = 15


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
