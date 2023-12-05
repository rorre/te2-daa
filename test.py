import gc
import json
import random
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Callable, NoReturn, ParamSpec, Tuple, TypeVar

import bnb
import dp

# We do manual garbage collection, so that the memory calculation isn't erroneous
gc.disable()

T = TypeVar("T")
P = ParamSpec("P")

# Start tracing memory allocations with tracemalloc
tracemalloc.start()


def measure_metric(f: Callable[P, T]) -> Callable[P, Tuple[int, float, T]]:
    """Decorator to wrap given function to measure the time and memory usage"""

    def wrapped(*args: P.args, **kwargs: P.kwargs):
        # Collect all garbage, set our gc to be in clean state before taking snapshot
        gc.collect()
        t_start = time.time()
        first = tracemalloc.take_snapshot()

        result = f(*args, **kwargs)

        second = tracemalloc.take_snapshot()
        t_end = time.time()

        # size_diff is in bytes, so we have to divide by 1024 later
        # t_end - t_start is in seconds
        return (
            second.compare_to(first, "filename")[0].size_diff,
            t_end - t_start,
            result,
        )

    return wrapped


# Wrap all of our test functions
brand_and_bound = measure_metric(bnb.unbounded_knapsack)
dynamic_programming = measure_metric(dp.unbounded_knapsack)
AlgorithmArgs = tuple[int, list[int], list[int]]


def test(args: AlgorithmArgs, data_size: int):
    """Tests given array and returns the result for both heapsort and randomized shell sort"""
    result = {
        "size": data_size,
        "bnb": {
            "memory": 0,
            "time": 0.0,
        },
        "dp": {
            "memory": 0,
            "time": 0.0,
        },
    }
    memory, t, value_bnb = brand_and_bound(*args)
    result["bnb"]["memory"] = memory
    result["bnb"]["time"] = t

    memory, t, value_dp = dynamic_programming(*args)
    result["dp"]["memory"] = memory
    result["dp"]["time"] = t

    assert value_bnb == value_dp, "Inconsistent result!"

    Path(f"dataset/{data_size}/").mkdir(exist_ok=True, parents=True)
    with open(f"dataset/{data_size}/result.json", "w") as f:
        json.dump(result, f)
    with open(f"dataset/{data_size}/dataset.json", "w") as f:
        json.dump(args, f)


def generate_dataset(size: int):
    """Generates dataset based on size"""
    W = size // 5

    # Upper bound is >= W to simulate some items being larger than weight
    val = [random.randint(1, int(W * 1.1)) for _ in range(size)]
    wt = [random.randint(1, int(W * 1.1)) for _ in range(size)]
    return W, val, wt


def help_and_exit() -> NoReturn:
    print(f"Usage: {sys.argv[0]} <size> [--reuse]")
    print("   size: array size")
    print("--reuse: reuse existing dataset")
    exit()


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        help_and_exit()

    size = int(sys.argv[1])
    if len(sys.argv) == 2:
        args = generate_dataset(size)

    else:
        if sys.argv[2] != "--reuse":
            help_and_exit()

        with open(f"dataset/{size}/dataset.json", "r") as f:
            args = json.load(f)

    test(args, size)
