# ba_meta require api 9
# ba_meta export babase.Plugin

from __future__ import annotations
from typing import TYPE_CHECKING
import babase as ba
import bauiv1 as bui
from bauiv1lib.ingamemenu import InGameMenuWindow

if TYPE_CHECKING:
    from typing import Any, Optional

# -----------------------------------------------------------------------------
# --- CUSTOMIZATION ---
# Change the numbers below to move the 'Get Gloves' button.
# 'x' moves it left (-) or right (+)
# 'y' moves it down (-) or up (+)
BUTTON_OFFSET = {'x': 0, 'y': 0}
# -----------------------------------------------------------------------------

# The main plugin class. BombSquad looks for this specifically.
# It MUST come immediately after the '# ba_meta export...' line above.
class MainPlugin(ba.Plugin):
    def __init__(self) -> None:
        patch_in_game_menu()

# --- All other code goes below the main plugin class ---

def get_player_spaz() -> Optional[ba.Actor]:
    """Finds the character of the local player."""
    activity = ba.get_foreground_host_activity()
    if activity:
        for player in activity.players:
            if player.is_alive() and player.sessionplayer.inputdevice.is_attached_to_player():
                return player.actor
    return None

def give_gloves() -> None:
    """The action for our button: find the player and give them gloves."""
    spaz = get_player_spaz()
    if spaz and hasattr(spaz, 'equip_boxing_gloves'):
        spaz.equip_boxing_gloves()
        ba.screenmessage("Gloves On!", color=(0, 1, 0))
        bui.getsound('powerup01').play()
    else:
        ba.screenmessage("You are not in the game!", color=(1, 0, 0))
        bui.getsound('error').play()

def patch_in_game_menu() -> None:
    """This function modifies the game's pause menu to add our button."""
    _old_init = InGameMenuWindow.__init__

    def _new_init(self: InGameMenuWindow, **kwargs: Any) -> None:
        _old_init(self, **kwargs)

        if self._root_widget.exists() and self._leave_button.exists():
            # Get the original position of the 'Leave Game' button.
            original_pos = self._leave_button.get_position()

            # Move the 'Leave Game' button up to make space.
            bui.buttonwidget(edit=self._leave_button, position=(original_pos[0], original_pos[1] + 50))
            
            # Calculate the new button's position using the offset from the top.
            new_button_pos = (
                original_pos[0] + BUTTON_OFFSET['x'],
                original_pos[1] + BUTTON_OFFSET['y']
            )

            # Add our new 'Get Gloves' button.
            bui.buttonwidget(
                parent=self._root_widget,
                position=new_button_pos,
                size=(160, 50),
                label='Get Gloves',
                on_activate_call=give_gloves,
                autoselect=True,
                scale=1.1,
                text_scale=1.2,
                color=(0.8, 0.2, 0.2)
            )
    
    InGameMenuWindow.__init__ = _new_init

