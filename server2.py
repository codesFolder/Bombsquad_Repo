# ba_meta require api 9
import babase
import bascenev1 as bs
from babase import Plugin as v
from bauiv1 import buttonwidget as z, gettexture as x
from bauiv1lib.ingamemenu import InGameMenuWindow as InGameMenu
from bauiv1lib.mainmenu import MainMenuWindow as MainMenu
import bauiv1 as bui

# ====== FAVOURITES LIST (auto-updated) ======
favourites = []
MAX_FAVS = 5  # how many favourites to keep
# ============================================

# Store last joined server
InGameMenu.i = InGameMenu.p = 0
_original_connect = bs.connect_to_party


def save_favourite(name, ip, port):
    global favourites
    new_entry = {"name": name, "ip": ip, "port": port}
    if new_entry not in favourites:
        favourites.append(new_entry)
        favourites = favourites[-MAX_FAVS:]


def reconnect(address, port=43210, print_progress=False):
    try:
        if bool(bs.get_connection_to_host_info_2()):
            bs.disconnect_from_host()
    except Exception:
        pass
    InGameMenu.i = address
    InGameMenu.p = port
    _original_connect(InGameMenu.i, InGameMenu.p, print_progress)
    babase.apptimer(1, check_and_save)


def check_and_save():
    info = bs.get_connection_to_host_info()
    if info and info.get('name'):
        save_favourite(info['name'], InGameMenu.i, InGameMenu.p)
    else:
        babase.apptimer(1, check_and_save)


def _draw_favourites_row(parent, width, start_y, color=(0.2, 0.6, 1)):
    """Draw a row (or two) of favourite buttons with wrapping."""
    if not favourites:
        return
    margin = 40
    btn_w, btn_h = 150, 40
    gap = 10
    x_pos = margin
    y_pos = start_y

    for fav in favourites:
        # Wrap to next row if we exceed safe width
        if x_pos + btn_w > width - margin:
            x_pos = margin
            y_pos += btn_h + gap  # next row upwards from bottom area

        z(
            parent=parent,
            size=(btn_w, btn_h),
            label=fav["name"][:22],
            color=color,
            on_activate_call=bs.Call(bs.connect_to_party, fav["ip"], fav["port"]),
            position=(x_pos, y_pos),
        )
        x_pos += btn_w + gap


# Add reconnect + favourites to in-game pause menu
def hook_ingame(func):
    def wrapper(self, *args, **kwargs):
        # First build the stock pause menu UI
        ret = func(self, *args, **kwargs)

        # Explicit, safe position for Reconnect: top-right corner
        z(
            parent=self._root_widget,
            size=(28, 28),
            icon=x('replayIcon'),
            color=(0, 1, 0),  # green
            position=(self._width - 60, self._height - 60),
            on_activate_call=bs.Call(reconnect, InGameMenu.i, InGameMenu.p),
            tooltip="Reconnect to last server",
        )

        # Favourites in pause menu:
        # place near bottom-left area, below/away from main actions.
        safe_bottom = 70  # above bottom info line
        _draw_favourites_row(
            parent=self._root_widget,
            width=self._width,
            start_y=safe_bottom,
            color=(0.2, 0.6, 1),
        )

        return ret
    return wrapper


# Draw favourites in main menu home screen (bottom-left row)
def hook_mainmenu(func):
    def wrapper(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)
        root = self._root_widget

        # Keep it consistent: bottom-left row on home screen
        _draw_favourites_row(
            parent=root,
            width=self._width,
            start_y=70,
            color=(0.2, 0.6, 1),
        )
        return ret
    return wrapper


# ba_meta export babase.Plugin
class byBordd(v):
    def __init__(self):
        InGameMenu._refresh_in_game = hook_ingame(InGameMenu._refresh_in_game)
        MainMenu._refresh = hook_mainmenu(MainMenu._refresh)
        bs.connect_to_party = reconnect
