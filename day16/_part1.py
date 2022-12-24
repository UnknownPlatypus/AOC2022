from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

reg = re.compile(r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnel.*valves* (.*)$")


def compute_bitwise_wizard_stuff(s: str) -> tuple[float, float]:
    tunnels = {}
    rates = {}
    for line in s.splitlines():
        parts = reg.match(line)
        assert parts is not None
        valve_name = parts[1]
        if parts[2] != "0":
            rates[valve_name] = int(parts[2])
        tunnels[valve_name] = parts[3].split(", ")

    I = {x: 1 << i for i, x in enumerate(rates)}  # noqa: E741
    T = {
        x: {y: 1 if y in tunnels[x] else float("+inf") for y in tunnels}
        for x in tunnels
    }
    for k in T:
        for i in T:
            for j in T:
                T[i][j] = min(T[i][j], T[i][k] + T[k][j])

    def visit(
        v: str,
        budget: float,
        state: int,
        flow: float,
        answer: dict[int, float],
    ) -> dict[int, float]:
        answer[state] = max(answer.get(state, 0), flow)
        for u in rates:
            newbudget = budget - T[v][u] - 1
            if I[u] & state or newbudget <= 0:
                continue
            visit(u, newbudget, state | I[u], flow + newbudget * rates[u], answer)
        return answer

    total1 = max(visit("AA", 30, 0, 0, {}).values())

    visited2 = visit("AA", 26, 0, 0, {})
    total2 = max(
        v1 + v2
        for k1, v1 in visited2.items()
        for k2, v2 in visited2.items()
        if not k1 & k2
    )

    return total1, total2


INPUT_S = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""
EXPECTED = 1651


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test_wizard(input_s: str, expected: int) -> None:
    assert compute_bitwise_wizard_stuff(input_s) == (1651, 1707)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute_bitwise_wizard_stuff(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
