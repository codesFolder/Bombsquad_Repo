# ba_meta require api 9
# ba_meta export babase.Plugin

from __future__ import annotations
from typing import TYPE_CHECKING
import babase as ba
import bauiv1 as bui
from bauiv1lib.ingamenu import InGameMenuWindow

if TYPE_CHECKING:
    from typing import Any, Optional

# THIS IS THE MAIN PLUGIN CLASS.
# IT MUST BE HERE, IMMEDIATELY AFTER THE '# ba_meta export' LINE.
class WorkingGlovesPlugin(ba.Plugin):
    def __init__(self) -> None:
        # This function will modify the game's menu.
        patch_in_game_menu()

# --- All other functions and code are defined below the main plugin class ---

def get_player_spaz() -> Optional[ba.Actor]:
    """Finds the character actor for the player using this device."""
    
    # We need to get the current 'activity' (the running game or menu)
    activity = ba.get_foreground_host_activity()
    if not activity:
        return None

    # Look through all players in the game.
    for player in activity.players:
        # Check if the player is alive and is the one using this instance of the game.
        if player.is_alive() and player.sessionplayer.inputdevice.is_attached_to_player():
            return player.actor
    return None

def give_gloves() -> None:
    """This is the simple function that runs when the button is clicked."""
    
    # Find the player's character in the game.
    spaz = get_player_spaz()

    # If we found the character and it's a valid character object...
    if spaz and hasattr(spaz, 'equip_boxing_gloves'):
        # ...give them gloves.
        spaz.equip_boxing_gloves()
        ba.screenmessage("Gloves On!", color=(0, 1, 0))
        bui.getsound('powerup01').play()
    else:
        # If not, show an error.
        ba.screenmessage("Could not find you in the game!", color=(1, 0, 0))
        bui.getsound('error').play()

def patch_in_game_menu() -> None:
    """This function safely modifies the game's pause menu."""

    # First, we store the original pause menu creation function.
    _old_init = InGameMenuWindow.__init__

    # Now, we create our new function that will replace the original.
    def _new_init(self: InGameMenuWindow, **kwargs: Any) -> None:
        
        # It's very important to call the original function first.
        # This builds the normal pause menu.
        _old_init(self, **kwargs)

        # We must check if the menu was created successfully before adding our button.
        if self._root_widget.exists() and self._leave_button.exists():
            
            # Get the position of the original 'Leave Game' button.
            pos = self._leave_button.get_position()

            # Move the original 'Leave Game' button up by 50 units to make space.
            bui.buttonwidget(edit=self._leave_button, position=(pos[0], pos[1] + 50))

            # Now, create our new 'Get Gloves' button in the empty space.
            bui.buttonwidget(
                parent=self._root_widget,
                position=pos, # Use the original position.
                size=(160, 50),
                label='Get Gloves',
                on_activate_call=give_gloves, # When clicked, run our simple function.
                autoselect=True,
                scale=1.1,
                text_scale=1.2,
                color=(0.8, 0.2, 0.2)
            )

    # Finally, we replace the game's original menu function with our new one.
    InGameMenuWindow.__init__ = _new_init
