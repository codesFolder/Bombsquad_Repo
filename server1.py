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

# Save a server to favourites
def save_favourite(name, ip, port):
    global favourites
    new_entry = {"name": name, "ip": ip, "port": port}
    if new_entry not in favourites:
        favourites.append(new_entry)
        favourites = favourites[-MAX_FAVS:]

# Reconnect function
def reconnect(address, port=43210, print_progress=False):
    try:
        if bool(bs.get_connection_to_host_info_2()):
            bs.disconnect_from_host()
    except:
        pass
    InGameMenu.i = address
    InGameMenu.p = port
    _original_connect(InGameMenu.i, InGameMenu.p, print_progress)
    babase.apptimer(1, check_and_save)

# Check connection and save to favourites
def check_and_save():
    info = bs.get_connection_to_host_info()
    if info and info.get('name'):
        save_favourite(info['name'], InGameMenu.i, InGameMenu.p)
    else:
        babase.apptimer(1, check_and_save)

# Add reconnect button to in-game menu
def hook_ingame(func):
    def wrapper(self, *args, **kwargs):
        z(
            parent=self._root_widget,
            size=(23, 26),
            icon=x('replayIcon'),
            color=(0, 1, 0),  # green
            on_activate_call=bs.Call(reconnect, InGameMenu.i, InGameMenu.p)
        )
        return func(self, *args, **kwargs)
    return wrapper

# Always draw favourites dynamically in main menu
def hook_mainmenu(func):
    def wrapper(self, *args, **kwargs):
        # First run the original menu build
        result = func(self, *args, **kwargs)

        # Then dynamically add favourites every time menu is shown
        root = self._root_widget
        start_x = 100
        y = self._height - 100

        for fav in favourites:
            z(
                parent=root,
                size=(150, 40),
                label=fav["name"][:18],
                color=(0.2, 0.6, 1),  # blue
                on_activate_call=bs.Call(bs.connect_to_party, fav["ip"], fav["port"]),
                position=(start_x, y)
            )
            start_x += 160

        return result
    return wrapper

# ba_meta export babase.Plugin
class byBordd(v):
    def __init__(self):
        InGameMenu._refresh_in_game = hook_ingame(InGameMenu._refresh_in_game)
        MainMenu._refresh = hook_mainmenu(MainMenu._refresh)
        bs.connect_to_party = reconnect
