from __future__ import annotations

import argparse
import operator
import os.path

import pytest
from z3 import Int, Optimize, sat

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

OP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def compute(s: str) -> int:
    o = Optimize()

    for line in s.splitlines():
        monk, operation = line.split(": ")
        parts = operation.split()
        if monk == "humn":  # it's me!
            continue
        elif len(parts) == 1:
            o.add(Int(monk) == int(parts[0]))
        elif monk == "root":
            o.add(Int(parts[0]) == Int(parts[2]))
        else:
            o.add(Int(monk) == OP[parts[1]](Int(parts[0]), Int(parts[2])))

    assert o.check() == sat
    return o.model()[Int("humn")].as_long()


INPUT_S = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""
EXPECTED = 301


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
