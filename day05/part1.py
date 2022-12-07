from __future__ import annotations

import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> str:
    crates, instructions = s.split("\n\n")
    lines = crates.splitlines()
    nb_stack = int(lines[-1].strip()[-1])
    stacks = [[] for _ in range(nb_stack)]  # type: ignore

    for line in reversed(crates.splitlines()):
        for i, crate in enumerate(line[1::4]):
            if crate != " ":
                stacks[i].append(crate)

    for instruction in instructions.split("\n")[:-1]:
        amount, start, end = (int(x) for x in instruction.split(" ")[1::2])
        moved_crates = reversed(stacks[start - 1][-amount:])
        del stacks[start - 1][-amount:]
        stacks[end - 1].extend(moved_crates)

    return "".join(stack[-1] for stack in stacks)


INPUT_S = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
EXPECTED = "CMZ"


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: str) -> None:
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
