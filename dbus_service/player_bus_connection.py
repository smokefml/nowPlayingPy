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
        self.bus: MessageBus | None = None # Tipado más específico
        self.props_interface: ProxyInterface | None = None
        self.player_interface: ProxyInterface | None = None # Tipado más específico
        self._connected = False # Nuevo flag para el estado de la conexión

    async def connect(self):
        if self._connected:
            return

        try:
            self.player_bus_name = await self.select_player(self.player_name)

            if not self.player_bus_name:
                raise Exception('No se detecta reproductores de medios.')

            self.bus = await MessageBus().connect()
            introspection = await self.bus.introspect(self.player_bus_name, self.obj_path)
            obj = self.bus.get_proxy_object(self.player_bus_name, self.obj_path, introspection)
            self.props_interface = obj.get_interface(self.iface_props)
            self.player_interface = obj.get_interface(self.iface_player)
            self._connected = True
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

    async def swap_player(self, new_player_name: str):
        await self.disconnect()
        self.player_name = new_player_name
        await self.connect()

    # ---- Control del reproductor (simplificado el manejo de errores) ------
    async def play_pause(self):
        try:
            await self.connect()
            await self.player_interface.call_play_pause() # type: ignore
        except Exception:
            await self.disconnect()

    async def next_track(self):
        try:
            await self.connect()
            await self.player_interface.call_next() # type: ignore
        except Exception:
            await self.disconnect()

    async def previous_track(self):
        try:
            await self.connect()
            await self.player_interface.call_previous() # type: ignore
        except Exception:
            await self.disconnect()

    async def stop(self):
        try:
            await self.connect()
            await self.player_interface.call_stop() # type: ignore
        except Exception:
            await self.disconnect()

    # ---- Obtener datos (Props) (Refactorizado para ser más robusto) -------
    async def get_prop(self, iface_string: str, prop_string: str, default=None):
        """Intenta obtener una propiedad, devuelve un valor por defecto si falla."""
        # Intenta conectar si no lo está. Si falla la conexión, devuelve el valor por defecto.
        try:
            await self.connect()
        except Exception:
            return default

        # Lógica específica de Firefox movida aquí para consistencia
        if "firefox" in self.player_bus_name and prop_string == "Volume": # type: ignore
            return default

        try:
            result = await self.props_interface.call_get(iface_string, prop_string) # type: ignore
            return result.value
        except DBusErrors.DBusError as e:
            # Captura errores D-Bus específicos y devuelve el valor por defecto
            if e.type in (DBusErrors.ErrorType.NOT_SUPPORTED, DBusErrors.ErrorType.INVALID_ARGS):
                return default
            # Para otros errores D-Bus, desconecta para forzar reconexión futura
            await self.disconnect()
            return default
        except Exception:
            # Captura cualquier otro error, desconecta y devuelve por defecto
            await self.disconnect()
            return default

    async def get_metadata(self):
        # Ahora el método get_prop maneja los errores y devuelve {} por defecto
        raw_meta = await self.get_prop(self.iface_player, 'Metadata', default={})
        if not raw_meta:
            return {}
        flat_meta = {k: v.value for k, v in raw_meta.items()}
        return flat_meta

    async def get_identity(self):
        identity = await self.get_prop('org.mpris.MediaPlayer2', 'Identity', default='Unknown')
        if not self._connected:
            return None
        return identity

    async def get_status(self):
        # Devuelve None si no se puede obtener el estado
        return await self.get_prop(self.iface_player, 'PlaybackStatus', default=None)

    async def get_position(self):
        # Devuelve 0 si no se puede obtener la posición
        return await self.get_prop(self.iface_player, 'Position', default=0)

    async def get_volume(self):
        # Devuelve None si no se puede obtener el volumen
        return await self.get_prop(self.iface_player, 'Volume', default=None)

    # ---- Desconectar antes de salir! ------------------
    async def disconnect(self):
        if self.bus:
            self.bus.disconnect()
        self.bus = None
        self.props_interface = None
        self.player_interface = None
        self._connected = False
