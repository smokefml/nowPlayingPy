# nowPlayingPy
TUI app made in Python for media player control, for players that support the MPRIS D-Bus spec

Connects with your favorite player or any player connected to D-Bus and shows its name, status, metadata such as title, artist and album, duration, current position in real time, volume... Also lets you control a few things such as pla/pause, go to next or previous track.
Shows everything in s slick terminal UI, using curses and Kitty's icat kitten for the cover. It only works on Linux since it uses MPRIS. I'm working on adding support for other terminal clients such as Alacritty.

## Requeriments

- Linux distro with D-Bus (most of them)
- Python 3
- kitty, the terminal client
- a terminal font patched with nerdfonts
- imagemagick
- python libraries:
    - python curses
    - python dbus-next
    - pyton nerdfonts
    - python wand
    - python requests
