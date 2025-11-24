import asyncio
from dbus_next.aio.message_bus import MessageBus
from dbus_next.aio.proxy_object import ProxyInterface
from dbus_next import errors as DBusErrors

from .bus_tasks import list_mpris_players

class PlayerBusConnection:
    def __init__(self, player_name_hint: str):
        self.player_name = player_name_hint.lower()
        self.player_bus_name = None
        self.obj_path = '/org/mpris/MediaPlayer2'
        self.iface_props = 'org.freedesktop.DBus.Properties'
        self.iface_player = 'org.mpris.MediaPlayer2.Player'
        self.bus = None
        self.props_interface: ProxyInterface | None = None
        self.player_interface = None

    async def connect(self):
        if self.bus is not None and self.props_interface is not None:
            return

        try:
            self.player_bus_name = await self.select_player(self.player_name)

            if not self.player_bus_name:
                raise Exception('No se detecta reproductores de medios.')

            self.bus = await MessageBus().connect()
            instrospection = await self.bus.introspect(self.player_bus_name, self.obj_path)
            obj = self.bus.get_proxy_object(self.player_bus_name, self.obj_path, instrospection)
            self.props_interface = obj.get_interface(self.iface_props)
            self.player_interface = obj.get_interface(self.iface_player)
        except Exception as e:
            await self.disconnect()
            raise e

    async def select_player(self, player_hint: str):
        players = await list_mpris_players()
        if not players:
            return None
        for player in players:
            if player_hint in player:
                return player
        return players[0]

    #---- Control del reproductor ----------------------
    async def play_pause(self):
        if self.player_interface:
            try:
                await self.player_interface.call_play_pause()
            except Exception:
                return

    async def next_track(self):
        if self.player_interface:
            try:
                await self.player_interface.call_next()
            except Exception:
                return

    async def previous_track(self):
        if self.player_interface:
            try:
                await self.player_interface.call_previous()
            except Exception:
                return

    async def stop(self):
        if self.player_interface:
            try:
                await self.player_interface.call_stop()
            except Exception:
                return

    #---- Obtener datos (Props) ------------------------
    async def get_prop(self, iface_string: str, prop_string: str):
        if self.props_interface is None:
            await self.connect()

        if "firefox" in self.player_bus_name and prop_string == "Volume":
            return None # Firefox does not support volume and we cant check safely

        try:
            return await self.props_interface.call_get(iface_string, prop_string) # Type: ignore
        except DBusErrors.DBusError as e:
            if e.type == DBusErrors.ErrorType.NOT_SUPPORTED:
                return None
            if e.type == DBusErrors.ErrorType.INVALID_ARGS:
                raise
            await self.disconnect()
            await asyncio.sleep(0.1)
            await self.connect()
            return await self.props_interface.call_get(iface_string, prop_string) # Type: ignore
        except Exception:
            raise

    async def get_metadata(self):
        metadata = await self.get_prop(self.iface_player, 'Metadata')

        if not metadata:
            return {}

        return metadata.value

    async def get_identity(self):
        identity = await self.get_prop('org.mpris.MediaPlayer2', 'Identity')

        if not identity:
            return self.player_name.title()

        return identity.value

    async def get_status(self):
        status = await self.get_prop(self.iface_player, 'PlaybackStatus')

        if not status:
            return None

        return status.value

    async def get_position(self):
        position = await self.get_prop(self.iface_player, 'Position')

        if not position:
            return 0

        return position.value

    async def get_volume(self):
        if self.props_interface:
            try:
                volume = await self.get_prop(self.iface_player, 'Volume')
                return volume.value
            except:
                pass
        return None

    #---- Desconectar antes de salir! ------------------
    async def disconnect(self):
        if self.bus:
            self.bus.disconnect()
            self.bus = None
            self.props_interface = None
