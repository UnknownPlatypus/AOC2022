from __future__ import annotations

import argparse
import os.path
from collections import Counter
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass(unsafe_hash=True)
class Sensor:
    x: int
    y: int
    x_b: int
    y_b: int

    @property
    def coverage(self) -> int:
        return abs(self.x - self.x_b) + abs(self.y - self.y_b)


def compute(s: str, max_range: int = 4000000) -> int:
    # 13615843289729
    # > 52697 ms
    sensors = set()
    for line in s.splitlines():
        parts = line.split(": closest beacon is at ")
        sensor_s = parts[0].split("Sensor at ")[1].split(", ")

        beacon_s = parts[1].split(", ")
        sensor = Sensor(
            x=int(sensor_s[0][2:]),
            y=int(sensor_s[1][2:]),
            x_b=int(beacon_s[0][2:]),
            y_b=int(beacon_s[1][2:]),
        )
        sensors.add(sensor)

    c: Counter[tuple[int, int]] = Counter()
    for sensor in sensors:
        top_y = sensor.y + sensor.coverage + 1
        bottom_y = sensor.y - sensor.coverage - 1
        left_x = sensor.x - sensor.coverage - 1
        right_x = sensor.x + sensor.coverage + 1

        # Find every location that are exactly one step outside
        # the sensor covered range. One must be common to all sensors.
        c.update(
            [
                (sensor.x, top_y),
                (sensor.x, bottom_y),
                (left_x, sensor.y),
                (right_x, sensor.y),
            ],
        )
        for i in range(1, sensor.coverage + 1):
            for x, y in (
                (sensor.x + i, top_y - i),
                (sensor.x - i, top_y - i),
                (sensor.x + i, bottom_y + i),
                (sensor.x - i, bottom_y + i),
            ):
                if x < 0 or y < 0 or x > max_range or y > max_range:
                    continue
                c[(x, y)] += 1
                if c[(x, y)] == 4:
                    print((x, y))
                    return x * 4000000 + y
    raise AssertionError


INPUT_S = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
EXPECTED = 56000011


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 20) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
