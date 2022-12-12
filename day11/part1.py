from __future__ import annotations

import argparse
import os.path
from dataclasses import dataclass
from functools import partial
from operator import add, mul
from typing import Callable

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class Monkey:
    items: list[int]
    op: Callable[[int], int]
    div: int
    if_true_target: int
    if_false_target: int
    nb_inspections: int = 0


def square(x: int) -> int:
    return x**2


def compute(s: str) -> int | None:
    # divide by 3 rounded after each inspection
    monks = []

    # Parse input
    for monkey_data in s.split("\n\n"):
        lines = monkey_data.splitlines()
        sign, val = lines[2].split("old ")[1].split()
        if val == "old":
            op = square
        elif sign == "+":
            op = partial(add, int(val))
        else:  # sign == "*"
            op = partial(mul, int(val))

        monks.append(
            Monkey(
                items=[int(s) for s in lines[1].split(": ")[1].split(", ")],
                op=op,
                div=int(lines[3].split("by ")[1]),
                if_true_target=int(lines[4].split("monkey ")[1]),
                if_false_target=int(lines[5].split("monkey ")[1]),
            ),
        )

    # Compute worry level
    for _ in range(20):
        for monk in monks:
            for item_worry_level in monk.items:
                monk.nb_inspections += 1

                worry_level = monk.op(item_worry_level) // 3
                if worry_level % monk.div == 0:
                    monks[monk.if_true_target].items.append(worry_level)
                else:
                    monks[monk.if_false_target].items.append(worry_level)

            monk.items = []  # Remove inspected items

    first, second = sorted(monk.nb_inspections for monk in monks)[-2:]
    return first * second


INPUT_S = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
EXPECTED = 10605


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
