from __future__ import annotations

import argparse
import os.path

import numpy as np
import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int | None:
    size = len(s.split("\n")[0]) - 2  # Sub matrix size
    total = 4 * (size + 1)
    tree_matrix = np.array([list(line) for line in s.splitlines()])
    visible_mat = [[False for _ in range(size)] for _ in range(size)]

    for i, line in enumerate(tree_matrix[1:-1]):  # Horizontal scan
        left_max = line[0]
        right_max = line[-1]

        for j, tree in enumerate(line[1:-1]):  # Left to right scan.
            if tree > left_max:
                left_max = tree
                visible_mat[i][j] = True
        for j, tree in enumerate(reversed(line[1:-1])):  # Right to left scan.
            if tree > right_max:
                right_max = tree
                visible_mat[i][size - 1 - j] = True

    visible_mat = np.rot90(visible_mat)
    for i, line in enumerate(np.rot90(tree_matrix)[1:-1]):  # Vertical scan
        left_max = line[0]
        right_max = line[-1]

        for j, tree in enumerate(line[1:-1]):  # Top to bottom scan.
            if tree > left_max:
                left_max = tree
                visible_mat[i][j] = True
        for j, tree in enumerate(reversed(line[1:-1])):  # Bottom to top scan.
            if tree > right_max:
                right_max = tree
                visible_mat[i][size - 1 - j] = True

    return total + np.count_nonzero(visible_mat)


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 21


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
