from __future__ import annotations

import argparse
import os.path

import numpy as np
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    tree_matrix = np.array([[int(tree) for tree in line] for line in s.splitlines()])

    def get_scenic_score(x: int, y: int) -> int:
        val = tree_matrix[x, y]
        left = right = up = down = 1

        for left, cand_y in enumerate(reversed(range(y)), start=1):
            if tree_matrix[x][cand_y] >= val:
                break

        for right, cand_y in enumerate(range(y + 1, size), start=1):
            if tree_matrix[x][cand_y] >= val:
                break

        for up, cand_x in enumerate(reversed(range(x)), start=1):
            if tree_matrix[cand_x][y] >= val:
                break

        for down, cand_x in enumerate(range(x + 1, size), start=1):
            if tree_matrix[cand_x][y] >= val:
                break

        return up * down * left * right

    size = len(tree_matrix[0])
    scores = set()

    for y in range(1, size):
        for x in range(1, size):
            scores.add(get_scenic_score(x, y))
    return max(scores)


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 8


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
