PLAYER_COUNT = 3

GRID_SIZE = 10

assert PLAYER_COUNT > 0
assert PLAYER_COUNT < 5
assert GRID_SIZE > 5

GRID_CENTER = GRID_SIZE // 2

EMPTY_BIOM = 0
SNOW = 1
DESSERT = 2
PLAINS = 3
FOREST = 4
MOUNTAINS = 5
VULCANO = 6

SPRING = 10  # (value >= spring) gives if the field has a spring, (value % spring) gives the biom
EMPTY_SHELL = 10

BIOMS = [SNOW, DESSERT, PLAINS, FOREST, MOUNTAINS, VULCANO]  # only for iteration over

BIOM_NAMES = [
    "EMPTY",  # EMPTY_BIOM
    "SCHNEE",  # SNOW
    "WÜSTE",  # DESERT
    "GRAß",  # PLAINS
    "WALD",  # FOREST
    "BERG",  # MOUNTAINS
    "VULKAN",  # VULCANO
]

COLORS = [
    "#000000",  # EMPTY_BIOM
    "#00bfff",  # SNOW
    "#ffd700",  # DESERT
    "#adff2f",  # PLAINS
    "#006400",  # FOREST
    "#3b3630",  # MOUNTAINS
    "#ff582e",  # VULCANO
]

NR_TOTAL_EGGS = [
    0,  # EMPTY_BIOM
    13,  # SNOW
    14,  # DESSERT
    12,  # PLAINS
    11,  # FOREST
    10,  # MOUNTAINS
    9,  # VULCANO
]

NR_DRAGONS_IN_EGGS = [
    0,  # EMPTY_BIOM
    7,  # SNOW
    7,  # DESSERT
    7,  # PLAINS
    7,  # FOREST
    7,  # MOUNTAINS
    7,  # VULCANO
]

# in format [tile_index, BiomIndex1, BiomIndex2]

STARTING_TILE = [0, DESSERT, SNOW, False, False]

TILES = [
    [0, EMPTY_BIOM, EMPTY_BIOM],  # index placeholder
    [1, SNOW + SPRING, PLAINS],
    [2, SNOW + SPRING, PLAINS],
    [3, SNOW, FOREST],
    [4, SNOW, FOREST],
    [5, SNOW, MOUNTAINS],
    [6, SNOW, MOUNTAINS],
    [7, SNOW + SPRING, SNOW],
    [8, PLAINS, FOREST],
    [9, PLAINS, FOREST],
    [10, PLAINS, MOUNTAINS],
    [11, PLAINS, MOUNTAINS],
    [12, PLAINS, VULCANO],
    [13, SNOW, VULCANO],
    [14, SNOW, VULCANO],
    [15, FOREST, MOUNTAINS],
    [16, FOREST, MOUNTAINS],
    [17, FOREST, VULCANO],
    [18, FOREST, VULCANO],
    [19, MOUNTAINS, VULCANO],
    [20, DESSERT, VULCANO],
    [21, DESSERT, VULCANO],
    [22, DESSERT + SPRING, PLAINS],
    [23, DESSERT + SPRING, PLAINS],
    [24, DESSERT, PLAINS + SPRING],
    [25, DESSERT, FOREST],
    [26, DESSERT, FOREST],
    [27, DESSERT, MOUNTAINS],
    [28, DESSERT + SPRING, DESSERT],
]
