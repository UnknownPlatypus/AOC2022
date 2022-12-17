from __future__ import annotations

import argparse
import heapq
import os.path
from collections import defaultdict
from string import ascii_lowercase

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int | None:
    end = (0, 0)

    lines = s.splitlines()
    size_x, size_y = len(lines), len(lines[0])

    # Get start and end position and normalize values.
    cells = {}
    for x, line in enumerate(lines):
        for y, letter in enumerate(line):
            if letter == "E":
                letter = "z"
                end = (x, y)
            if letter == "S":
                letter = "a"
            cells[(x, y)] = ascii_lowercase.index(letter)

    # Compute possible moves from every position.
    moves = defaultdict(list)
    for (x, y), value in cells.items():
        if (y < size_y - 1) and (value - cells[x, y + 1]) <= 1:  # RIGHT
            moves[(x, y)].append((x, y + 1))

        if (y > 0) and (value - cells[x, y - 1]) <= 1:  # LEFT
            moves[(x, y)].append((x, y - 1))

        if (x < size_x - 1) and (value - cells[x + 1, y]) <= 1:  # UP
            moves[(x, y)].append((x + 1, y))

        if (x > 0) and (value - cells[x - 1, y]) <= 1:  # DOWN
            moves[(x, y)].append((x - 1, y))

    # Dijkstra shortest path implementation using heapq
    seen = set()
    todo = [(0, end)]

    while todo:
        cost, point = heapq.heappop(todo)
        if cells[point] == 0:  # ascii_lowercase.index("a")
            return cost
        elif point in seen:
            continue
        else:
            seen.add(point)

        for next_place in moves[point]:
            if cells[next_place] - cells[point] >= -1:
                heapq.heappush(todo, (cost + 1, next_place))


INPUT_S = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
EXPECTED = 29


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
