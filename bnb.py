import math
from typing import Literal, NamedTuple

State = Literal["DEVELOP", "BACKTRACK", "REPLACE", "END"]


class Item(NamedTuple):
    value: int
    weight: int


class KnapsackSolve:
    def __init__(self, W: int, items: list[Item]):
        self.W = W
        self.items = items
        self.n = len(items)

        # Will be initialized in init()
        self.M: list[list[int]]
        self.xhat: list[int]
        self.zhat: int

        self.x: list[int]
        self.i: int
        self.vn: int
        self.W0: int
        self.U: int
        self.m: list[int]

    def eliminate_dominated_items(self):
        N = set(range(self.n))
        for j in range(self.n - 1):
            for k in range(j + 1, self.n):
                if math.floor(self.items[k].weight / self.items[j].weight) * self.items[j].value >= self.items[k].value:
                    N = N - {k}
                elif (
                    math.floor(self.items[j].weight / self.items[k].weight) * self.items[k].value >= self.items[j].value
                ):
                    N = N - {j}
                    break

        self.items = [self.items[i] for i in N]
        self.n = len(self.items)

    def calc_u(self, i: int):
        if i + 2 >= self.n:
            return self.vn

        z0 = self.vn + math.floor(self.W0 / self.items[i + 1].weight) * self.items[i + 1].weight
        W1 = self.W0 - math.floor(self.W0 / self.items[i + 1].weight) * self.items[i + 1].weight
        U0 = z0 + math.floor(W1 * self.items[i + 2].value / self.items[i + 2].weight)

        tmp = W1 + math.ceil((1 / self.items[i].weight) * (self.items[i + 1].weight - W1)) * self.items[i].weight
        U1 = z0 + math.floor(
            tmp * self.items[i + 1].value / self.items[i + 1].weight
            - math.ceil((1 / self.items[i].weight * (self.items[i + 1].weight - W1))) * self.items[i].value
        )

        return max(U0, U1)

    def init(self):
        # Eliminate dominated items according to Procedure 1.
        self.eliminate_dominated_items()

        # Sort the non-dominated items according to decreasing vi/wi ratios
        self.items.sort(key=lambda x: x.value / x.weight, reverse=True)

        # xhat = 0; x = 0; i = 1; zhat = 0
        self.xhat = [0 for _ in range(self.n)]
        self.zhat = 0
        self.x = [0 for _ in range(self.n)]
        self.i = 0

        # Initialize empty sparse matrix M
        self.M = [[0 for _ in range(self.W + 1)] for _ in range(self.n)]

        # x1 = floor(W/w1), V(N) = v1x1, W0 = W–w1x1
        self.x[0] = self.W // self.items[0].weight
        self.vn = self.items[0].value * self.x[0]
        self.W0 = self.W - self.items[0].weight * self.x[0]

        # Calculate U
        self.U = self.calc_u(self.i)
        self.zhat = self.vn
        self.xhat = self.x.copy()

        self.m: list[int] = []
        for z in range(self.n):
            min_weight = math.inf
            for j, item in enumerate(self.items):
                if j > z and item.weight < min_weight:
                    min_weight = item.weight

            self.m.append(min_weight)  # type: ignore

    def develop(self):
        if self.W0 < self.m[self.i]:
            if self.zhat < self.vn:
                self.zhat = self.vn
                self.xhat = self.x.copy()
                if self.zhat == self.U:
                    return "END"

            return "BACKTRACK"

        # Else block here
        j: int | None = None
        for j in range(self.i + 1, self.n):
            if self.items[j].weight <= self.W0:
                j = j
                break

        if j is None:
            return "BACKTRACK"

        if self.vn + self.calc_u(j) <= self.zhat:
            return "BACKTRACK"

        if self.M[self.i][self.W0] >= self.vn:
            return "BACKTRACK"

        self.x[j] = math.floor(self.W0 / self.items[j].weight)
        self.vn += self.items[j].value * self.x[j]
        self.W0 -= self.items[j].weight * self.x[j]

        self.M[self.i][self.W0] = self.vn
        self.i = j
        return "DEVELOP"

    def backtrack(self):
        j = self.i
        while j <= self.i and j >= 0:
            if self.x[j] > 0:
                break

            j -= 1

        if j == -1:
            return "END"

        self.i = j
        self.x[self.i] -= 1
        self.vn -= self.items[self.i].value
        self.W0 += self.items[self.i].weight

        if self.W0 < self.m[self.i]:
            return "BACKTRACK"

        if self.vn + math.floor(self.W0 * self.items[self.i + 1].value / self.items[self.i + 1].weight) <= self.zhat:
            self.vn -= self.items[self.i].value * self.x[self.i]
            self.W0 += self.items[self.i].weight * self.x[self.i]
            self.x[self.i] = 0
            return "BACKTRACK"

        if self.W0 - self.items[self.i].weight >= self.m[self.i]:
            return "DEVELOP"

        return "REPLACE"

    def replace_item(self):
        j = self.i
        h = j + 1
        while True:
            if h >= self.n:
                return "BACKTRACK"

            if self.zhat >= self.vn + math.floor(self.W0 * self.items[h].value / self.items[h].weight):
                return "BACKTRACK"

            if self.items[h].weight >= self.items[j].weight:
                if (
                    (self.items[h].weight == self.items[j].weight)
                    or (self.items[h].weight > self.W0)
                    or (self.zhat >= self.vn + self.items[h].value)
                ):
                    h += 1
                    continue

                self.zhat = self.vn + self.items[h].value
                self.xhat = self.x.copy()

                self.x[h] = 1
                if self.zhat == self.calc_u(h):
                    return "END"

                j = h
                h += 1
                continue

            if self.W0 - self.items[h].weight < self.m[h - 1]:
                h += 1
                continue

            self.i = h
            self.x[self.i] = self.W0 // self.items[self.i].weight

            self.vn += self.items[self.i].value * self.x[self.i]
            self.W0 -= self.items[self.i].weight * self.x[self.i]
            return "DEVELOP"

    def solve(self):
        self.init()
        next_action: State = "DEVELOP"
        while next_action != "END":
            if next_action == "DEVELOP":
                next_action = self.develop()

            if next_action == "BACKTRACK":
                next_action = self.backtrack()

            if next_action == "REPLACE":
                next_action = self.replace_item()
        return self.xhat, self.zhat


def unbounded_knapsack(W: int, val: list[int], wt: list[int]):
    items = list(map(Item, val, wt))
    solver = KnapsackSolve(W, items)
    return solver.solve()[1]
