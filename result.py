import json

SIZES = (100, 1000, 10000)


def print_result():
    for size in SIZES:
        print(size)
        try:
            with open(f"dataset/{size}/result.json") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("ERR: Cannot found result file, did the test fail?")
            print("------------------")
            continue

        print(
            "Branch and Bound",
            f'{round(data["bnb"]["time"] * 1000)}ms',
            f'{round(data["bnb"]["memory"] / 1024, 3)}KiB',
        )
        print(
            "Dynamic Programming",
            f'{round(data["dp"]["time"] * 1000)}ms',
            f'{round(data["dp"]["memory"] / 1024, 3)}KiB',
        )
        print("------------------")


if __name__ == "__main__":
    print_result()
