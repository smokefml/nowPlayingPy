import curses
import nerdfonts as nf

def chop_string(s:str, lg:int):
    return [s[i:i+lg] for i in range(0, len(s), lg)]

def draw_info(window: curses.window, info, ui_attr):
    player, title, artist, album, album_art_path, length, position, volume, status = info.values()
    base_color, header_color, separator_color, key_color, value_color, time_bar_color, volume_bar_color, empty_bar_color, separator_length, separator_char, bar_char, key_indent, time_bar_length, volume_bar_length = ui_attr.values()
    status_icon = '󰐎'
    volume_icon = ''
    title_icon = '󰎇'
    artist_icon = '󰠃'
    album_icon = '󰀥'
    time_icon = '󱫜'

    if status == 'Playing':
        status_icon = nf.icons['fa_play']
    elif status == 'Paused':
        status_icon = nf.icons['fa_pause']
    else:
        status_icon = nf.icons['fa_stop']

    if length > 0:
        percent = position * 100 / length
    else:
        percent = 100
    filled = int(percent * time_bar_length / 100)
    empty = int(time_bar_length - filled)

    #window.addstr(0,0, "cover: {}".format(album_art_path))

    # Separator
    window.hline(2, key_indent, separator_char, separator_length, separator_color)

    # If no players
    if player == 'STOP' and status == 'STOP':
        window.addstr(1, key_indent, "{}  Not Playing"
                      .format(status_icon),
                      curses.color_pair(1) | curses.A_BOLD
                      )
        window.addstr(3, key_indent, "{}  {}"
                      .format(nf.icons['fa_exclamation_triangle'], title), 
                      value_color | curses.A_BOLD
                      )

        window.refresh()
        return

    # Header
    window.addstr(1, key_indent, "{}  {} {}"
                  .format(status_icon, status, player),
                  header_color | curses.A_BOLD
                  )

    # key: value
    title_key = "{}  Title: ".format(title_icon)
    artist_key = "{}  Artist: ".format(artist_icon)
    album_key = "{}  Album: ".format(album_icon)
    pos_dur_key = "{}  ".format(time_icon)
    if title and not artist and not album:
        action = '{}  Watching: '.format(nf.icons['fa_film'])
        if ' - YouTube' in title:
            title = title.replace(" - YouTube", "")
            action = action = '{}  YouTube: '.format(nf.icons['fa_youtube_play'])
        title_chunks = chop_string(title, 32)
        window.addstr(3, key_indent, action, key_color)
        window.addstr(3, key_indent + len(action), title_chunks[0], value_color)
        if len(title_chunks) >= 2:
            window.addstr(4, key_indent + 3, "{}".format(title_chunks[1]), value_color)
        if len(title_chunks) >= 3:
            window.addstr(5, key_indent + 3, "{}".format(title_chunks[2]), value_color)
    else:
        window.addstr(3, key_indent, title_key, key_color | curses.A_BOLD)
        window.addstr(3, key_indent + len(title_key), title, value_color)
        window.addstr(4, key_indent, artist_key, key_color | curses.A_BOLD)
        window.addstr(4, key_indent + len(artist_key), artist, value_color)
        window.addstr(5, key_indent, album_key, key_color | curses.A_BOLD)
        window.addstr(5, key_indent + len(album_key), album, value_color)

    window.addstr(7, key_indent, pos_dur_key, key_color | curses.A_BOLD)
    window.addstr(7, key_indent + len(pos_dur_key), "{:02d}:{:02d} / {:02d}:{:02d}"
        .format(
            int(position/60), int(position%60),
            int(length/60), int(length%60)), value_color)
    window.hline(8, key_indent + 3, bar_char, filled, time_bar_color)
    window.hline(8, key_indent + filled + 3 , bar_char, empty, empty_bar_color)

    if volume:
        if volume == 0.0:
            volume_icon = nf.icons['fa_volume_off']
        elif volume <= 0.6:
            volume_icon = nf.icons['fa_volume_down']
        elif volume > 0.6:
            volume_icon = nf.icons['fa_volume_up']
        volume_key = "{}  Volume: ".format(volume_icon)
        window.addstr(10, key_indent, volume_key, key_color | curses.A_BOLD)
        window.addstr(10, key_indent + len(volume_key), "{}%"
                      .format(int(volume * 100)), value_color
        )
        window.hline(
            11, key_indent + 3,
            bar_char,
            int(volume * volume_bar_length),
            volume_bar_color
        )
        window.hline(
            11, key_indent + int(volume * volume_bar_length) + 3,
            bar_char,
            int(volume_bar_length - volume * volume_bar_length),
            empty_bar_color
        )

    window.refresh()
