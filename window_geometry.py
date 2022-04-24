local_window_width = 650
local_window_height = 350
local_spacing = 30

online_window_width = 450
online_window_height = 200
online_spacing = 25

window_geometry = {
    "local": [
        str(int(local_window_width))
        + "x"
        + str(int(local_window_height))
        + "+"
        + str(int(local_window_width) * 0)
        + "+"
        + str(int(local_window_height) * 0),
        str(int(local_window_width))
        + "x"
        + str(int(local_window_height))
        + "+"
        + str(int(local_window_width))
        + "+"
        + str(int(local_window_height) * 0),
        str(int(local_window_width))
        + "x"
        + str(int(local_window_height))
        + "+"
        + str(int(local_window_width) * 0)
        + "+"
        + str(int(local_window_height) * 1 + local_spacing),
        str(int(local_window_width))
        + "x"
        + str(int(local_window_height))
        + "+"
        + str(int(local_window_width))
        + "+"
        + str(int(local_window_height) * 1 + local_spacing),
        str(int(local_window_width))
        + "x"
        + str(int(local_window_height))
        + "+"
        + str(int(local_window_width * 0.25))
        + "+"
        + str(int(local_window_height * 0.25)),
    ],
    "browser": [
        str(int(online_window_width))
        + "x"
        + str(int(online_window_height))
        + "+"
        + str(int(online_window_width) * 0)
        + "+"
        + str(int(online_window_height) * 0),
        str(int(online_window_width))
        + "x"
        + str(int(online_window_height))
        + "+"
        + str(int(online_window_width))
        + "+"
        + str(int(online_window_height) * 0),
        str(int(online_window_width))
        + "x"
        + str(int(online_window_height))
        + "+"
        + str(int(online_window_width) * 0)
        + "+"
        + str(int(online_window_height) * 1 + online_spacing),
        str(int(online_window_width))
        + "x"
        + str(int(online_window_height))
        + "+"
        + str(int(online_window_width))
        + "+"
        + str(int(online_window_height) * 1 + online_spacing),
        str(int(online_window_width))
        + "x"
        + str(int(online_window_height))
        + "+"
        + str(int(online_window_width * 0.25))
        + "+"
        + str(int(online_window_height * 0.25)),
    ],
}