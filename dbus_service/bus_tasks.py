from dbus_next.aio.message_bus import MessageBus

async def list_mpris_players():
    try:
        bus = await MessageBus().connect()

        introspection = await bus.introspect('org.freedesktop.DBus', '/org/freedesktop/DBus')
        proxy_obj = bus.get_proxy_object('org.freedesktop.DBus', '/org/freedesktop/DBus', introspection)
        dbus_interface = proxy_obj.get_interface('org.freedesktop.DBus')

        names = await dbus_interface.call_list_names()

        mpris_players = [name for name in names if name.startswith('org.mpris.MediaPlayer2') and name != 'org.mpris.MediaPlayer2']

        bus.disconnect()
    except Exception as e:
        print(f"Error al acceder al bus: {e}")
        mpris_players = []

    return mpris_players
