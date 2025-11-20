import curses
import nerdfonts as nf

def chop_string(s:str, lg:int):
    return [s[i:i+lg] for i in range(0, len(s), lg)]

def draw_info(window: curses.window, column: int, info):
    player, title, artist, album, album_art_path, length, position, volume, status = info.values()

    status_icon = '󰐎'
    volume_icon = ''
    title_icon = '󰎇'
    artist_icon = '󰠃'
    album_icon = '󰀥'
    time_icon = '󱫜'
    youtube_icon = ''

    if status == 'Playing':
        status_icon = nf.icons['fa_play']
    elif status == 'Paused':
        status_icon = nf.icons['fa_pause']
    else:
        status_icon = nf.icons['fa_stop']

    time_bar_length = 30
    if length > 0:
        percent = position * 100 / length
    else:
        percent = 100
    filled = int(percent * time_bar_length / 100)
    empty = int(time_bar_length - filled)

    #window.addstr(0,0, "cover: {}".format(album_art_path))

    window.hline(2, column, curses.ACS_HLINE, 38)

    if player == 'STOP' and status == 'STOP':
        window.addstr(1, column, "{}  Not Playing"
                      .format(status_icon),
                      curses.color_pair(1) | curses.A_BOLD
                      )
        window.addstr(3, column, "{}  {}"
                      .format(nf.icons(['fa_warning']), title), curses.A_BOLD
                      )

        window.refresh()
        return

    window.addstr(1, column, "{}  {} {}"
                  .format(status_icon, status, player),
                  curses.color_pair(5) | curses.A_BOLD
                  )

    if ' - YouTube' in title and not artist and not album:
        title_chunks = chop_string(title.replace(" - YouTube", ""), 32)
        window.addstr(3, column, "{}  YouTube: {}"
                      .format(youtube_icon, title_chunks[0]))
        if len(title_chunks) >= 2:
            window.addstr(4, column + 3, "{}".format(title_chunks[1]))
        if len(title_chunks) >= 3:
            window.addstr(5, column + 3, "{}".format(title_chunks[2]))
    else:
        window.addstr(3, column, "{}  Title: {}"
                      .format(title_icon, title), curses.A_BOLD)
        window.addstr(4, column, "{}  Artist: {}"
                      .format(artist_icon, artist))
        window.addstr(5, column, "{}  Album: {}"
                      .format(album_icon, album))

    window.addstr(7, column, "{}  {:02d}:{:02d} / {:02d}:{:02d}".format(
        time_icon,
        int(position/60),
        int(position%60),
        int(length/60),
        int(length%60)
        ))
    window.hline(8, column + 3, curses.ACS_HLINE, filled, curses.color_pair(3))
    window.hline(8, column + filled + 3 , curses.ACS_HLINE, empty, curses.color_pair(6))

    if volume:
        if volume == 0.0:
            volume_icon = ''
        elif volume <= 0.6:
            volume_icon = ''
        elif volume > 0.6:
            volume_icon = ''
        vol_bar_length = 20
        window.addstr(10, column, "{}  Volume: {}%".format(
            volume_icon,
            int(volume * 100)
            ))
        window.hline(
            11, column + 3,
            curses.ACS_HLINE,
            int(volume * vol_bar_length),
            curses.color_pair(4)
        )
        window.hline(
            11, column + int(volume * vol_bar_length) + 3,
            curses.ACS_HLINE,
            int(vol_bar_length - volume * vol_bar_length),
            curses.color_pair(6)
        )

    window.refresh()
