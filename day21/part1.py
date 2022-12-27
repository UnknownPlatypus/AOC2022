from __future__ import annotations

import argparse
import operator
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

OP = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


def compute(s: str) -> int:
    monks = {}
    todos = set()

    for line in s.splitlines():
        monk, operation = line.split(": ")
        parts = operation.split()
        if len(parts) == 1:
            monks[monk] = int(parts[0])
        else:
            todos.add((monk, parts[0], OP[parts[1]], parts[2]))

    todo = deque(todos)
    while todo:
        monk, m1, op, m2 = todo.popleft()

        if m1 in monks and m2 in monks:
            monks[monk] = op(monks[m1], monks[m2])
            if monk == "root":
                return monks[monk]
        else:
            todo.append((monk, m1, op, m2))

    raise AssertionError("unreachable")


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
EXPECTED = 152


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
