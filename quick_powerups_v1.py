# ba_meta require api 9

import babase as ba
import bauiv1 as bui
import bascenev1 as bs
from bauiv1lib.ingamenu import InGameMenuWindow

# --- All functions are defined first, before the final plugin class ---

def get_player_spaz():
    """Finds the character of the local player."""
    activity = ba.get_foreground_host_activity()
    if activity:
        for player in activity.players:
            if player.is_alive() and player.sessionplayer.inputdevice.is_attached_to_player():
                return player.actor
    return None

def give_gloves() -> None:
    """The action for the button: find the player and give them gloves."""
    spaz = get_player_spaz()
    if spaz and hasattr(spaz, 'equip_boxing_gloves'):
        spaz.equip_boxing_gloves()
        ba.screenmessage("Gloves On!", color=(0, 1, 0))
        bui.getsound('powerup01').play()
    else:
        ba.screenmessage("Could not find character!", color=(1, 0, 0))
        bui.getsound('error').play()

def patch_menu_to_add_button(original_function):
    """This function takes the original menu code and adds our button to it."""
    
    def new_function(self, *args, **kwargs):
        # First, run the original menu code.
        original_function(self, *args, **kwargs)
        
        # Now, add our new button to the already-created menu.
        bui.buttonwidget(
            parent=self._root_widget,
            size=(160, 50),
            label='Get Gloves',
            on_activate_call=give_gloves,
            autoselect=True,
            scale=1.1,
            text_scale=1.2,
            color=(0.8, 0.2, 0.2),
            # Position it relative to the leave button to avoid conflicts.
            position=(self._leave_button.get_position()[0], self._leave_button.get_position()[1] - 60)
        )
            
    return new_function

# ba_meta export babase.Plugin
# This is the final and most important part.
# The game looks for this exact line, and the class MUST come immediately after it.
class FinalPlugin(ba.Plugin):
    def __init__(self):
        # Replace the game's menu function with our modified one.
        InGameMenuWindow._refresh_in_game = patch_menu_to_add_button(
            InGameMenuWindow._refresh_in_game
        )

