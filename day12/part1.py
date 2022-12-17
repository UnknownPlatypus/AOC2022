from __future__ import annotations

import argparse
import heapq
import os.path
from collections import defaultdict
from string import ascii_lowercase

import networkx as nx
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int | None:
    start = end = (0, 0)

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
                start = (x, y)
            cells[(x, y)] = ascii_lowercase.index(letter)

    # Compute possible moves from every position.
    moves = defaultdict(list)
    for (x, y), value in cells.items():
        if (y < size_y - 1) and (value - cells[x, y + 1]) >= -1:
            moves[(x, y)].append((0, 1))

        if (y > 0) and (value - cells[x, y - 1]) >= -1:
            moves[(x, y)].append((0, -1))

        if (x < size_x - 1) and (value - cells[x + 1, y]) >= -1:
            moves[(x, y)].append((1, 0))

        if (x > 0) and (value - cells[x - 1, y]) >= -1:
            moves[(x, y)].append((-1, 0))

    # Dijkstra shortest path implementation using heapq
    seen = set()
    todo = [(0, start)]

    while todo:
        cost, point = heapq.heappop(todo)

        if point == end:
            return cost
        elif point in seen:
            continue
        else:
            seen.add(point)

        for possible_move in moves[point]:
            next_place = point[0] + possible_move[0], point[1] + possible_move[1]
            if cells[next_place] - cells[point] <= 1:
                heapq.heappush(todo, (cost + 1, next_place))


def compute_nx(s: str) -> int:
    # Actually 2x slower due to the Graph building part
    start = end = (0, 0)

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
                start = (x, y)
            cells[(x, y)] = ascii_lowercase.index(letter)

    # Build a graph from all possible edges
    G = nx.DiGraph()
    for (x, y), value in cells.items():
        if (y < size_y - 1) and (value - cells[x, y + 1]) >= -1:
            G.add_edge((x, y), (x, y + 1))

        if (y > 0) and (value - cells[x, y - 1]) >= -1:
            G.add_edge((x, y), (x, y - 1))

        if (x < size_x - 1) and (value - cells[x + 1, y]) >= -1:
            G.add_edge((x, y), (x + 1, y))

        if (x > 0) and (value - cells[x - 1, y]) >= -1:
            G.add_edge((x, y), (x - 1, y))

    return nx.dijkstra_path_length(G, source=start, target=end)


INPUT_S = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
EXPECTED = 31


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test2(input_s: str, expected: int) -> None:
    assert compute_nx(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    with open(args.data_file) as f, support.timing():
        print(compute_nx(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
