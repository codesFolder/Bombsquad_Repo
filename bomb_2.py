# ba_meta require api 9
from __future__ import annotations
from typing import TYPE_CHECKING

import babase
import bascenev1 as bs

if TYPE_CHECKING:
    from typing import Any

# --- CONFIGURATION ---
# You can change these values to customize the plugin.

# The time in seconds that the bomb timer starts from.
BOMB_START_TIME = 9.0

# The position of the timer text relative to the bomb's center.
# Format is (X, Y, Z). Y is the vertical axis.
TIMER_POSITION_OFFSET = (0, 1.2, 0)

# --- END OF CONFIGURATION ---


# We need to save the original Bomb methods before we replace them.
_old_bomb_init = bs.Bomb.__init__
_old_bomb_del = bs.Bomb.__del__


def _new_bomb_init(self,
                   position: tuple[float, float, float] = (0.0, 1.0, 0.0),
                   velocity: tuple[float, float, float] = (0.0, 0.0, 0.0),
                   bomb_type: str = 'normal',
                   blast_radius: float = 2.0,
                   source_player: bs.Player | None = None,
                   owner: bs.Node | None = None):
    """
    This function will run every time a new bomb is created.
    """
    # First, call the original __init__ to make sure the bomb is
    # created correctly by the game engine.
    _old_bomb_init(self, position, velocity, bomb_type, blast_radius,
                   source_player, owner)

    # Now, add our custom timer logic.
    self._bomb_timer_countdown = BOMB_START_TIME

    # Create the floating text node.
    self._bomb_timer_text_node = babase.newnode(
        'text',
        owner=self.node,  # Attach it to the bomb's node.
        attrs={
            'text': f'{self._bomb_timer_countdown:.1f}',
            'in_world': True,  # Make it a 3D object in the game world.
            'shadow': 0.5,
            'flatness': 1.0,
            'scale': 0.012,
            'h_align': 'center',
            'color': (1, 1, 0.4) # A light yellow color
        })
    
    # Start the timer loop that will update the text.
    self._bomb_timer = babase.AppTimer(
        0.1, babase.Call(self._update_bomb_timer), repeat=True
    )


def _update_bomb_timer(self) -> None:
    """
    This function runs every 0.1 seconds for each bomb.
    """
    self._bomb_timer_countdown -= 0.1

    # Safety check: Make sure the text node still exists before trying to edit it.
    if self._bomb_timer_text_node:
        if self._bomb_timer_countdown > 0:
            # Update the text with the new time, formatted to one decimal place.
            self._bomb_timer_text_node.text = f'{self._bomb_timer_countdown:.1f}'
        else:
            # Once time is up, show 0.0 and stop updating.
            self._bomb_timer_text_node.text = '0.0'
            self._bomb_timer = None # Stop the timer loop.

def _new_bomb_del(self) -> None:
    """
    This runs when a bomb is destroyed (explodes, falls, etc.).
    """
    # Clean up our custom timer and text node to prevent memory leaks.
    self._bomb_timer = None
    if self._bomb_timer_text_node:
        self._bomb_timer_text_node.delete()

    # Call the original __del__ to let the game finish deleting the bomb.
    _old_bomb_del(self)


# ba_meta export babase.Plugin
class BombTimerPlugin(babase.Plugin):
    """
    A plugin to display a countdown timer above bombs.
    """
    def __init__(self):
        # This is where we apply the "monkey-patch".
        # We replace the game's default functions with our new ones.
        bs.Bomb.__init__ = _new_bomb_init
        bs.Bomb.__del__ = _new_bomb_del
        bs.Bomb._update_bomb_timer = _update_bomb_timer
