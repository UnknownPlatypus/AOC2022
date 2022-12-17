from __future__ import annotations

import argparse
import os.path
from collections import defaultdict
from pathlib import Path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int | None:

    current_dir = Path("/")
    dirs: dict[Path, dict[str, int]] = {current_dir: {}}
    for line in s.splitlines():
        if line.startswith("$ "):  # instruction
            cmd = line.rsplit("$ ")[1].split()

            if cmd[0] != "ls":
                target = cmd[1]
                if target == "..":
                    current_dir = current_dir.parents[0]
                else:
                    current_dir /= target
                dirs.setdefault(current_dir, {})
        else:
            # ls output
            dir_or_size, filename = line.split()
            if dir_or_size != "dir":  # file
                dirs[current_dir][filename] = int(dir_or_size)

    dir_sizes: defaultdict[Path, int] = defaultdict(int)
    for path, dic in dirs.items():
        current_dir_size = sum(dic.values())
        dir_sizes[path] += current_dir_size
        for sub_path in path.parents:
            dir_sizes[sub_path] += current_dir_size

    threshold = 30000000 - (70000000 - dir_sizes[Path("/")])
    return next(
        size
        for dir_name, size in sorted(dir_sizes.items(), key=lambda item: item[1])
        if size > threshold
    )


INPUT_S = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
EXPECTED = 24933642


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
