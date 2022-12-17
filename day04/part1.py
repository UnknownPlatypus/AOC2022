from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    overlap = 0

    for line in s.splitlines():
        elf1, elf2 = line.split(",")
        elf1_x, elf1_y = (int(v) for v in elf1.split("-"))
        elf2_x, elf2_y = (int(v) for v in elf2.split("-"))

        if elf1_x <= elf2_x <= elf2_y <= elf1_y or elf2_x <= elf1_x <= elf1_y <= elf2_y:
            overlap += 1
    return overlap


INPUT_S = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
EXPECTED = 2


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
