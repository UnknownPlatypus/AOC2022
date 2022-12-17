from __future__ import annotations

import argparse
import ast
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compare(e1: list | int, e2: list | int) -> int:
    """
    return < 0 -> Good order
    return > 0 -> bad order
    return 0 -> equal
    """
    if isinstance(e1, int) and isinstance(e2, int):
        return e1 - e2
    elif isinstance(e1, int):
        e1 = [e1]
    elif isinstance(e2, int):
        e2 = [e2]

    if isinstance(e1, list) and isinstance(e2, list):
        for a, b in itertools.zip_longest(e1, e2):
            if a is None:  # e1 shorter
                return -1
            elif b is None:  # e2 shorter
                return 1

            diff = compare(a, b)
            if diff != 0:
                return diff
        return 0
    else:
        raise TypeError("Trust me mypy, nothing to see here.")


def compute(s: str) -> int:
    packet_pairs = s.split("\n\n")

    tot = 0
    for i, packet in enumerate(packet_pairs, start=1):
        s1, s2 = packet.splitlines()
        l1 = ast.literal_eval(s1)
        l2 = ast.literal_eval(s2)

        if compare(l1, l2) <= 0:
            tot += i

    return tot


INPUT_S = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
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

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
