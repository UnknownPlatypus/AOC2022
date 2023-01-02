from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

vals = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}


def snafu_to_int(s: str) -> int:
    return sum(vals[char] * 5**i for i, char in enumerate(s[::-1]))


def int_to_snafu(nb: int) -> str:
    snafu: list[str] = []

    while nb:
        mod = nb % 5
        if mod <= 2:
            snafu += str(mod)
        elif mod == 3:
            snafu += "="
            nb += mod
        elif mod == 4:
            snafu += "-"
            nb += mod

        nb //= 5
    return "".join(reversed(snafu))


def compute(s: str) -> str:
    print("\n")
    nb = sum(snafu_to_int(line) for line in s.splitlines())
    return int_to_snafu(nb)


INPUT_S = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""
EXPECTED = "2=-1=0"


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
