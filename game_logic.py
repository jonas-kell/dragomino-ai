ACTION_SET_TILE = "ACTION_SET_TILE"


def action_handler(player, game_state, action, **args):
    print("Player " + str(player) + " wants action: " + action)
    print(game_state)

    if action == ACTION_SET_TILE:
        print(args)
    else:
        raise Exception("Unsupported Action: " + action)


def action_player_injector(player, game_state):
    return lambda action, **args: action_handler(player, game_state, action, **args)