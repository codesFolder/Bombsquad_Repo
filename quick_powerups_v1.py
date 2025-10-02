# ba_meta require api 9
# (see https://ballistica.net/wiki/meta-tag-system)

"""
Quick Powerups Plugin
A simple plugin to quickly give yourself powerups during a game.
Inspired by the powerful Sandbox mod, but simplified for ease of use.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import babase as ba
import bauiv1 as bui
from bauiv1lib.ingamemenu import InGameMenuWindow

if TYPE_CHECKING:
    from typing import Any, Optional


# A simple class to store our settings
class PluginSettings:
    """Stores the state of the 'permanent' checkbox."""
    is_permanent: bool = False


def get_player_spaz() -> Optional[ba.Actor]:
    """
    Finds and returns the Spaz (character) of the local player.
    Returns None if the player doesn't have a character in the game.
    """
    activity = ba.get_foreground_host_activity()
    if activity:
        for player in activity.players:
            # Check if the player is alive and is controlled by the local device
            if player.is_alive() and player.sessionplayer.inputdevice.is_attached_to_player():
                return player.actor
    return None


def apply_powerup(powerup_type: str) -> None:
    """Applies a powerup to the local player's character."""
    spaz = get_player_spaz()
    if not spaz:
        ba.screenmessage("You are not in the game!", color=(1, 0, 0))
        bui.getsound('error').play()
        return

    # Use direct equipment for permanent effect, or PowerupMessage for temporary
    if PluginSettings.is_permanent:
        if powerup_type == 'punch':
            spaz.equip_boxing_gloves()
        elif powerup_type == 'triple_bombs':
            spaz.set_bomb_count(3)
        elif powerup_type == 'shield':
            spaz.equip_shields()
        # For other powerups, the temporary message is the only way
        else:
            spaz.handlemessage(ba.PowerupMessage(poweruptype=powerup_type))
    else:
        spaz.handlemessage(ba.PowerupMessage(poweruptype=powerup_type))

    ba.screenmessage(f"Applied {powerup_type.replace('_', ' ').title()}",
                     color=(0, 1, 0))
    bui.getsound('powerup01').play()


class PowerupSelectWindow(bui.Window):
    """A window to select from a list of all available powerups."""

    def __init__(self):
        self._width = 450
        self._height = 350
        self._scroll_width = self._width - 100
        self._scroll_height = self._height - 120
        self._sub_width = self._scroll_width
        self._sub_height = 800  # A large height to fit all buttons

        # Define the powerups we want to show
        self.powerups = [
            'triple_bombs', 'health', 'ice_bombs',
            'impact_bombs', 'punch', 'shield', 'sticky_bombs'
        ]

        super().__init__(root_widget=bui.containerwidget(
            size=(self._width, self._height),
            transition='in_right',
            scale=1.5,
            stack_offset=(0, -10)
        ))

        # Close button
        self._cancel_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(40, self._height - 60),
            size=(50, 50),
            scale=0.8,
            label='',
            on_activate_call=self._on_cancel_press,
            autoselect=True,
            color=(0.5, 0.4, 0.6),
            icon=bui.gettexture('crossOut'),
            iconscale=1.2)
        bui.containerwidget(edit=self._root_widget,
                            cancel_button=self._cancel_button)

        bui.textwidget(parent=self._root_widget,
                       position=(self._width * 0.5, self._height - 40),
                       size=(0, 0),
                       text="All Powerups",
                       color=bui.app.ui_v1.title_color,
                       h_align='center',
                       v_align='center',
                       maxwidth=200)

        # Scrollable area for the powerup list
        self._scrollwidget = bui.scrollwidget(
            parent=self._root_widget,
            position=(50, 50),
            size=(self._scroll_width, self._scroll_height),
            autoselect=True)
        bui.containerwidget(edit=self._scrollwidget, claims_left_right=True)
        self._subcontainer = bui.containerwidget(
            parent=self._scrollwidget,
            size=(self._sub_width, self._sub_height),
            background=False)

        # Create a button for each powerup
        v_offset = self._sub_height
        for i, powerup in enumerate(self.powerups):
            v_offset -= 60
            bui.buttonwidget(
                parent=self._subcontainer,
                position=(0, v_offset),
                size=(self._sub_width, 50),
                label=powerup.replace('_', ' ').title(),
                autoselect=True,
                on_activate_call=ba.Call(
                    self.select_powerup, powerup
                )
            )

    def select_powerup(self, powerup_type: str) -> None:
        """Called when a powerup button is pressed."""
        apply_powerup(powerup_type)
        self._on_cancel_press()

    def _on_cancel_press(self) -> None:
        bui.containerwidget(edit=self._root_widget, transition='out_right')


class QuickPowerupsWindow(bui.Window):
    """The main window for the plugin."""

    def __init__(self, origin_widget: bui.Widget):
        self._width = 400
        self._height = 250
        super().__init__(root_widget=bui.containerwidget(
            size=(self._width, self._height),
            transition='in_right',
            scale=2.0,
            stack_offset=(0, -10)
        ))

        # We want to close the main in-game menu when we open this
        bui.containerwidget(edit=origin_widget, transition='out_left')

        # Window Title
        bui.textwidget(parent=self._root_widget,
                       position=(self._width * 0.5, self._height - 40),
                       size=(0, 0),
                       text="Quick Powerups",
                       color=bui.app.ui_v1.title_color,
                       h_align='center',
                       v_align='center',
                       maxwidth=250)

        # Main quick button
        bui.buttonwidget(
            parent=self._root_widget,
            position=(50, self._height - 120),
            size=(self._width - 100, 60),
            label="Boxing Gloves & Triple Bombs",
            on_activate_call=self.apply_combo,
            autoselect=True)

        # Button for more options
        bui.buttonwidget(
            parent=self._root_widget,
            position=(50, self._height - 180),
            size=(self._width - 100, 40),
            label="Choose Other Powerups...",
            on_activate_call=self.open_powerup_select)

        # Checkbox for 'permanent' mode
        bui.checkboxwidget(
            parent=self._root_widget,
            text='Permanent (Lasts until death)',
            position=(50, 40),
            size=(self._width - 100, 30),
            value=PluginSettings.is_permanent,
            on_value_change_call=self.on_permanent_change,
            autoselect=True)

        # Close button
        self._back_button = bui.buttonwidget(
            parent=self._root_widget,
            position=(self._width - 70, self._height - 60),
            size=(50, 50),
            scale=0.8,
            label='',
            on_activate_call=self.close,
            autoselect=True,
            color=(0.5, 0.4, 0.6),
            icon=bui.gettexture('crossOut'),
            iconscale=1.2)
        bui.containerwidget(edit=self._root_widget,
                            cancel_button=self._back_button)

    def on_permanent_change(self, value: bool) -> None:
        """Update the setting when the checkbox is clicked."""
        PluginSettings.is_permanent = value

    def apply_combo(self) -> None:
        """Applies the main combo and closes the window."""
        apply_powerup('punch')
        apply_powerup('triple_bombs')
        self.close()

    def open_powerup_select(self) -> None:
        """Opens the list of all powerups."""
        self.close()
        PowerupSelectWindow()

    def close(self) -> None:
        """Closes the window."""
        bui.containerwidget(edit=self._root_widget, transition='out_right')


# This is the tricky part: we 'patch' the game's existing menu window
# to add our own button.

# Store the original function.
_old_in_game_menu_init = InGameMenuWindow.__init__


def _new_in_game_menu_init(self: InGameMenuWindow, **kwargs: Any) -> None:
    """Our modified version of the function."""
    # First, call the original function to build the menu as usual.
    _old_in_game_menu_init(self, **kwargs)

    # Add a print statement to the console to confirm the plugin is running
    ba.print("Quick Powerups Plugin: Attempting to add button to menu.")

    # Now, add our custom button.
    # We'll shift the existing 'Leave' button up to make space.
    if self._leave_button.exists():
        ba.print(
            "Quick Powerups Plugin: Found 'Leave' button, adding powerup button.")
        pos = self._leave_button.get_position()
        bui.buttonwidget(edit=self._leave_button,
                         position=(pos[0], pos[1] + 50))

        # Add our button where the 'Leave' button used to be.
        bui.buttonwidget(
            parent=self._root_widget,
            position=pos,
            size=(160, 50),
            label='Quick Powerups',
            on_activate_call=ba.Call(QuickPowerupsWindow, self._root_widget),
            autoselect=True,
            scale=1.1,
            text_scale=1.2,
            color=(0.1, 0.5, 0.8))
    else:
        ba.print(
            "Quick Powerups Plugin: Could not find 'Leave' button. Button not added.")


# Overwrite the game's original function with our new one.
InGameMenuWindow.__init__ = _new_in_game_menu_init

