PLAYER_COUNT = 3

GRID_SIZE = 10

assert PLAYER_COUNT > 0
assert PLAYER_COUNT < 5
assert GRID_SIZE > 5

GRID_CENTER = GRID_SIZE // 2

SNOW = 0
DESSERT = 1
PLAINS = 2
FOREST = 3
MOUNTAINS = 4
VULCANO = 5

COLORS = [
    "#00bfff",  # SNOW
    "#ffd700",  # DESERT
    "#adff2f",  # PLAINS
    "#006400",  # FOREST
    "#3b3630",  # MOUNTAINS
    "#ff582e",  # VULCANO
]

TOTAL_EGGS = [
    13,  # SNOW
    14,  # DESSERT
    12,  # PLAINS
    11,  # FOREST
    10,  # MOUNTAINS
    9,  # VULCANO
]

NR_DRAGONS_IN_EGGS = [
    7,  # SNOW
    7,  # DESSERT
    7,  # PLAINS
    7,  # FOREST
    7,  # MOUNTAINS
    7,  # VULCANO
]

# in format [tile_index, BiomIndex1, BiomIndex2, SpringOn1, SpringOn2]

STARTING_TILE = [0, DESSERT, SNOW, False, False]

TILES = [
    [1, SNOW, PLAINS, True, False],
    [2, SNOW, PLAINS, True, False],
    [3, SNOW, FOREST, False, False],
    [4, SNOW, FOREST, False, False],
    [5, SNOW, MOUNTAINS, False, False],
    [6, SNOW, MOUNTAINS, False, False],
    [7, SNOW, SNOW, True, False],
    [8, PLAINS, FOREST, False, False],
    [9, PLAINS, FOREST, False, False],
    [10, PLAINS, MOUNTAINS, False, False],
    [11, PLAINS, MOUNTAINS, False, False],
    [12, PLAINS, VULCANO, False, False],
    [13, SNOW, VULCANO, False, False],
    [14, SNOW, VULCANO, False, False],
    [15, FOREST, MOUNTAINS, False, False],
    [16, FOREST, MOUNTAINS, False, False],
    [17, FOREST, VULCANO, False, False],
    [18, FOREST, VULCANO, False, False],
    [19, MOUNTAINS, VULCANO, False, False],
    [20, DESSERT, VULCANO, False, False],
    [21, DESSERT, VULCANO, False, False],
    [22, DESSERT, PLAINS, True, False],
    [23, DESSERT, PLAINS, True, False],
    [24, DESSERT, PLAINS, False, True],
    [25, DESSERT, FOREST, False, False],
    [26, DESSERT, FOREST, False, False],
    [27, DESSERT, MOUNTAINS, False, False],
    [28, DESSERT, DESSERT, True, False],
]
