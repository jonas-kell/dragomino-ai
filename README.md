# Dragomino Ai

Graphic interface to assist with the playing of the game [Dragomino](https://pegasusshop.de/sortiment/spiele/kinderspiele/11649/dragomino-kinderspiel-des-jahres-2021) [Spiel-Des-Jahres](https://www.spiel-des-jahres.de/spiele/dragomino/).

Calculates probabilities on the fly.
Even includes a basic predition method trying to advise on the best placement of the next tile.

Prediction is not very sophisicated as of now, because more time was spent getting the ui ready then I thought.

# History

This was done as a time-passing project during a vacation on a mountain hut.
Therefore the challange basically was not to google anything, as the is basically no network connection.
As of this, some of the code may be a little rough around the edges.

# Installation

To be run locally, this needs `python3` as well as the python library `tkinter`.
Otherwise no dependencies are needed.

Just run the `main.py` script:

```
python main.py
```

# Run in the browser

This project can be run with [REPLIT](https://replit.com/). Just klick [HERE](https://replit.com/@jonas-kell/dragomino-ai).

You can minimize The `file` panel. Clicking `RUN` should be sufficient. Sometimes you need to click on the App-Arrow and the RUN button and sometimes you need to solve a captcha.

On a chrome-browser with a 4k-Monitor zooming to `250%` and going to fullscreen (`F11`) looks best.

Sadly repositioning windows doesn't work on replit, but at least they're somewhat resized to the correct dimensions.

# Usage

Number of players can be adjusted via the `PLAYER_COUNT` variable in `game_constants.py`. I sady have not yet fount a good way to make it dynamic.

Tiles can be selected with leftclick on the main window. Then the predictions get shown in the player windows.
Tiles can be placed with leftclick in the player-windows. The first selected tile will be placed.
To place a different one, deselect tiles in the main window.

Tiles can be rotated with right click during placing.

If no tile is selected, shells/dragons can be toggled with rightclick on matching connections.
