from __future__ import annotations

import argparse
import os.path
from collections import Counter
from string import ascii_letters

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    # Another possibility is to use set intersection again.~
    total = 0

    lines = s.splitlines()
    for i in range(len(lines) // 3):
        counter = Counter(set(lines[3 * i]))
        counter.update(set(lines[3 * i + 1]))
        counter.update(set(lines[3 * i + 2]))
        letter = counter.most_common(1)[0][0]
        total += ascii_letters.index(letter) + 1

    return total


INPUT_S = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
EXPECTED = 70


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
