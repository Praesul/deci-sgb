import random

import numpy as np


def order_targets(primary_target: tuple, secondary_targets: list[tuple]):
    pass


def iter_arrows(dummy: tuple, grid: np.ndarray) -> np.ndarray:
    """
    Increment 4 locations on the grid adjacent to dummy_position.
    For each increment, attempt up to 5 times to find a location with a value of 0 before
    using the last attempted location.
    """
    grid[dummy[0]][dummy[1]] += 1

    arrow_count = 0
    while arrow_count < 4:
        arrow_attempts = 0
        while arrow_attempts < 5:
            y_shift = random.randint(-1, 1)
            x_shift = random.randint(-1, 1)
            arrow = (dummy[0] + y_shift, dummy[1] + x_shift)

            if grid[arrow[0], arrow[1]] == 0 or arrow_attempts == 4:
                grid[arrow[0], arrow[1]] += 1
                break
            else:
                arrow_attempts += 1

        arrow_count += 1
    return grid


def iter_dummies(dummies: list[tuple], grid: np.ndarray | None = None) -> np.ndarray:
    """
    Create a grid of 0's and iterate through the dummy locations, casting sgb at each.
    Optionally, provide a preexisting grid to accommodate players casting sgb after each other.
    """
    if grid is None:
        grid = np.zeros((9, 9), dtype=int)

    for dummy in dummies:
        grid = iter_arrows(dummy, grid)
    return grid


def count_arrows_landed(npc_size: int, npc_sw: tuple, grid: np.ndarray) -> int:
    arrows_landed = 0
    for i in range(npc_sw[0] - npc_size + 1, npc_sw[0] + 1):
        for j in range(npc_sw[1], npc_sw[1] + npc_size):
            arrows_landed += grid[i][j]
    return arrows_landed


def calc_sgb(
    dummies: list[tuple],
    npc_sw: tuple,
    npc_size: int = 3,
    n_players: int = 1,
) -> float:
    grid = np.zeros((9, 9), dtype=int)
    for _ in range(n_players):
        grid = iter_dummies(dummies, grid)
        # print(grid)

    arrows_landed = 1
    for i in range(npc_sw[0] - npc_size + 1, npc_sw[0] + 1):
        for j in range(npc_sw[1], npc_sw[1] + npc_size):
            if (i, j) in dummies:
                arrows_landed += 0.5 * (grid[i][j] - 1)
            else:
                arrows_landed += grid[i][j]
    return arrows_landed / n_players


def run_monte_carlo(
    dummies: list[tuple],
    npc_sw: tuple,
    npc_size: int = 3,
    n_players: int = 1,
    n_simulations: int = 2000,
) -> float:
    total_arrows = 0.0
    for _ in range(n_simulations):
        arrows_landed = calc_sgb(dummies, npc_sw, npc_size, n_players)
        total_arrows += arrows_landed
    return total_arrows / n_simulations


def draw_dummies(dummies: list[tuple]):
    """
    Display the dummy locations in a 2d array.
    """
    grid = np.zeros((9, 9), dtype=int)
    for dummy in dummies:
        grid[dummy[0]][dummy[1]] += 1
    print(grid)


def test_config(dummies: list[tuple], npc_sw, message: str):
    """
    Run multiple tests on a particular dummy layout and average it.
    """
    arrows_landed = run_monte_carlo(
        dummies,
        npc_sw,
        n_players=6,
        n_simulations=2000,
    )
    draw_dummies(dummies)
    print(f"{message} avg. arrows: {round(arrows_landed, 2)}")


def p4_configs():
    test_config(
        [(3, 4), (3, 5), (4, 4), (4, 4), (4, 5), (5, 3), (5, 5)],
        (4, 4),
        "P4 current dummies",
    )
    test_config(
        [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 4), (4, 5)],
        (4, 4),
        "P4 block south dummies Solak S",
    )
    test_config(
        [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 4), (4, 5)],
        (4, 4),
        "P4 block dummies Solak S",
    )
    test_config(
        [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (4, 5)],
        (4, 5),
        "P4 block dummies Solak SE",
    )
    test_config(
        [(3, 3), (3, 4), (3, 5), (4, 3), (3, 4), (4, 4), (4, 5)],
        (3, 4),
        "P4 block dummies Solak N",
    )
    test_config(
        [(3, 3), (3, 4), (3, 5), (4, 3), (3, 5), (4, 4), (4, 5)],
        (3, 5),
        "P4 block dummies Solak NE",
    )
    test_config(
        [(3, 3), (5, 3), (3, 5), (5, 5), (4, 4), (4, 4), (3, 4)],
        (4, 4),
        "X dummies extra N",
    )
    test_config(
        [(3, 3), (5, 3), (3, 5), (5, 5), (4, 4), (4, 4), (4, 5)],
        (4, 4),
        "X dummies extra E",
    )
    test_config(
        [(3, 3), (5, 3), (3, 5), (5, 5), (4, 4), (4, 4), (5, 4)],
        (4, 4),
        "X dummies extra S",
    )
    test_config(
        [(3, 3), (5, 3), (3, 5), (5, 5), (4, 4), (4, 4), (4, 3)],
        (4, 4),
        "X dummies extra W",
    )


if __name__ == "__main__":
    # P1 configurations
    test_config([(3, 3), (3, 4), (3, 5), (4, 4), (4, 5), (3, 4)], (3, 4), "P1 dummies")
    test_config([(2, 3), (3, 3), (4, 3), (4, 4), (4, 5), (3, 4)], (3, 4), "L dummies")

    # P2 configurations
    test_config([(3, 3), (5, 3), (3, 5), (5, 5), (4, 4), (4, 4)], (4, 4), "P2 dummies")

    p4_configs()
