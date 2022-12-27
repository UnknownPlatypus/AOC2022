from __future__ import annotations

import argparse
import collections
import math
import os.path
import re
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

reg = re.compile(
    r"^Blueprint \d+: Each ore robot costs (\d+) ore. "
    r"Each clay robot costs (\d+) ore. "
    r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
    r"Each geode robot costs (\d+) ore and (\d+) obsidian.$",
)


class Cost(NamedTuple):
    ore_bot_ore: int
    cla_bot_ore: int
    obs_bot_ore: int
    obs_bot_cla: int
    geo_bot_ore: int
    geo_bot_obs: int


class State(NamedTuple):
    depth: int
    nb_ore_b: int
    nb_clay_b: int
    nb_obs_b: int
    nb_geo_b: int
    nb_ore: int
    nb_clay: int
    nb_obs: int
    nb_geo: int


def compute_one(items: re.Match) -> int:
    cost = Cost(
        ore_bot_ore=int(items[1]),
        cla_bot_ore=int(items[2]),
        obs_bot_ore=int(items[3]),
        obs_bot_cla=int(items[4]),
        geo_bot_ore=int(items[5]),
        geo_bot_obs=int(items[6]),
    )

    max_ore = max(
        cost.ore_bot_ore,
        cost.cla_bot_ore,
        cost.obs_bot_ore,
        cost.geo_bot_ore,
    )

    todo = collections.deque([(0, 1, 0, 0, 0, 0, 0, 0, 0)])
    seen = set()  # Track step already processed
    best_nb_geo = 0

    while todo:
        state = todo.popleft()
        (
            depth,
            nb_ore_b,
            nb_clay_b,
            nb_obs_b,
            nb_geo_b,
            nb_ore,
            nb_clay,
            nb_obs,
            nb_geo,
        ) = state
        new_depth = depth + 1

        if new_depth == 33:
            best_nb_geo = max(best_nb_geo, nb_geo)

        nb_ore = min(max_ore * (32 - depth), nb_ore)
        nb_clay = min(cost.obs_bot_cla * (32 - depth), nb_clay)
        nb_obs = min(cost.geo_bot_obs * (32 - depth), nb_obs)
        nb_ore_b = min(nb_ore_b, max_ore)
        nb_clay_b = min(nb_clay_b, cost.obs_bot_cla)
        nb_obs_b = min(nb_obs_b, cost.geo_bot_obs)

        if state in seen or new_depth == 33:
            continue
        else:
            seen.add(state)

        new_nb_ore = nb_ore + nb_ore_b
        new_nb_clay = nb_clay + nb_clay_b
        new_nb_obs = nb_obs + nb_obs_b
        new_nb_geo = nb_geo + nb_geo_b

        # Buy geo if possible
        if nb_ore >= cost.geo_bot_ore and nb_obs >= cost.geo_bot_obs:
            todo.append(
                (
                    new_depth,
                    nb_ore_b,
                    nb_clay_b,
                    nb_obs_b,
                    nb_geo_b + 1,
                    new_nb_ore - cost.geo_bot_ore,
                    new_nb_clay,
                    new_nb_obs - cost.geo_bot_obs,
                    new_nb_geo,
                ),
            )
            continue

        # Buy obs
        if nb_ore >= cost.obs_bot_ore and nb_clay >= cost.obs_bot_cla:
            todo.append(
                (
                    new_depth,
                    nb_ore_b,
                    nb_clay_b,
                    nb_obs_b + 1,
                    nb_geo_b,
                    new_nb_ore - cost.obs_bot_ore,
                    new_nb_clay - cost.obs_bot_cla,
                    new_nb_obs,
                    new_nb_geo,
                ),
            )
        # Buy clay
        if nb_ore >= cost.cla_bot_ore:
            todo.append(
                (
                    new_depth,
                    nb_ore_b,
                    nb_clay_b + 1,
                    nb_obs_b,
                    nb_geo_b,
                    new_nb_ore - cost.cla_bot_ore,
                    new_nb_clay,
                    new_nb_obs,
                    new_nb_geo,
                ),
            )
        # Buy ore
        if nb_ore >= cost.ore_bot_ore:
            todo.append(
                (
                    new_depth,
                    nb_ore_b + 1,
                    nb_clay_b,
                    nb_obs_b,
                    nb_geo_b,
                    new_nb_ore - cost.ore_bot_ore,
                    new_nb_clay,
                    new_nb_obs,
                    new_nb_geo,
                ),
            )
        # Buy nothing
        todo.append(
            (
                new_depth,
                nb_ore_b,
                nb_clay_b,
                nb_obs_b,
                nb_geo_b,
                new_nb_ore,
                new_nb_clay,
                new_nb_obs,
                new_nb_geo,
            ),
        )

    print(f"Done with {items[0].split(':')[0]}: {best_nb_geo}")
    return best_nb_geo


def compute(s: str) -> int:
    return math.prod(
        compute_one(reg.match(line))  # type: ignore
        for i, line in enumerate(s.splitlines()[:3], start=1)
    )


INPUT_S = """\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
EXPECTED = 33


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
