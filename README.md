# nowPlayingPy
TUI app made in Python for media player control, for players that support the MPRIS D-Bus spec

Connects with your favorite player or any player connected to D-Bus and shows its name, status, metadata such as title, artist and album, duration, current position in real time, volume... Also lets you control a few things such as play/pause, go to next or previous track.
Shows everything in a slick terminal UI, using curses and Kitty's icat kitten for the cover. It only works on Linux since it uses MPRIS. I'm working on adding support for other terminal clients such as Alacritty.

## How to run
Simply download/clone this repo

```bash
git clone https://github.com/smokefml/nowPlayingPy.git
```

Navigate to the downloaded folder

```bash
cd nowPlayingPy
```

And you can run it simply with

```bash
./start.sh
```

The script will take care of Python's virtual environment and dependencies for you

## Config
Through config.json file

- app
  - favorite_player: any string that may be part of your default player's bus name (e.g. vlc)
- ui
  - cover
    - size: integer, cover width in characters (e.g. 36 will draw a square of 36 console characters wide)
    - method: only "icat" supported for now
    - position: "left" or "right" (still not implemented, has no effect)
- draw_borders: true or false, to draw the window borders, or not
- separator
  - character: "default" or any single character used to draw the divider under the header line
  - length: integer, length of this divider
- bars
  - character: "default" or any single character used to draw the position and volume bars
  - position_length: integer, length of the position bar
  - volume_length: integer, length of the volume bar
- no_colors: if true, everything becomes white on black background, ignoring the "colors" section
- colors: color strings may be a default term color like "black" or a hex rgb color "#aabbcc"
  - background: bg color, for every element
  - foreground: fg color, affects the borders, if toggled on
  - header_color: color of the header or "status player_name" zone
  - separator_color: color of the divider under the header
  - key_color: color of the labels and icons (name, artist, album, etc)
  - value_color: color of the information contents (right side of the key: value pairs)
  - time_bar_color: color of the position bar (filled part)
  - volume_bar_color: color of the volume bar (filled part)
  - empty_bar_color: color of the empty side (right) of every bar

## Requirements

### System deps
- Linux distro with D-Bus (most of them)
- Python 3
- kitty, the terminal client
- a terminal font patched with nerdfonts
- imagemagick

### python deps
- curses
- dbus-next
- nerdfonts
- wand
- requests
