from game_constants import *

ACTION_SET_TILE = "ACTION_SET_TILE"


def action_handler(global_update_callback, player, game_state, action, **args):
    print("Player " + str(player) + " wants action: " + action)

    # print(game_state)

    if action == ACTION_SET_TILE:
        tile = TILES[2]
        game_state[player][0][args["gy"], args["gx"]] = tile[0]
        game_state[player][0][args["gy"], args["gx"] + 1] = tile[1]
    else:
        raise Exception("Unsupported Action: " + action)

    # print(game_state)

    # trigger global update
    global_update_callback()


def action_player_injector(global_update_callback, player, game_state):
    return lambda action, **args: action_handler(
        global_update_callback, player, game_state, action, **args
    )