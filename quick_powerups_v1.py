# ba_meta require api 9
import babase
import _babase
import bauiv1 as bui
import bascenev1 as bs
from bascenev1 import broadcastmessage as push
from bauiv1lib.ingamemenu import InGameMenuWindow as igm
from bascenev1lib.actor.playerspaz import PlayerSpaz


class NicePowerup:
    """Main class similar to how sandbox.py uses Nice class"""
    
    # Define the same colors as sandbox
    cola = (0.13, 0.13, 0.13)
    colb = cola
    wht = (1, 1, 1)

    def __init__(self):
        # Apply the patch to the InGameMenu
        self.patch_igm()

    def patch_igm(self):
        """Patch the InGameMenu to add our powerup button like sandbox does"""
        original_method = igm._refresh_in_game

        def patched_method(self, *args, **kwargs):
            # Call the original method first
            result = original_method(self, *args, **kwargs)

            # Add our powerup button like sandbox does for its buttons
            self.powerup_button = bui.buttonwidget(
                parent=self._root_widget,
                position=(100, self._height - 180),
                size=(100, 40),
                label='Powerups',
                color=self.colb,
                textcolor=self.wht,
                on_activate_call=self.open_powerup_panel,
                button_type='square'
            )
            
            return result

        igm._refresh_in_game = patched_method

    def open_powerup_panel(self):
        PowerupPanel()


class PowerupPanel:
    """UI class to handle the powerup panel"""
    
    def __init__(self):
        # Use same colors as sandbox
        self.cola = NicePowerup.cola
        self.colb = NicePowerup.colb
        self.wht = NicePowerup.wht
        self._create_ui()
        
    def _create_ui(self):
        """Create the powerup panel UI following the sandbox.py structure"""
        # Get the overlay stack
        overlay_stack = bui.get_special_widget('overlay_stack')
        
        # Create the main container like in sandbox
        self._container = bui.containerwidget(
            parent=overlay_stack,
            size=(300, 250),
            position=(100, 300),
            scale=1.0,
            color=self.cola,  # Same as sandbox's cola color
            transition='in_right'
        )
        
        # Title like in sandbox
        bui.textwidget(
            parent=self._container,
            text='Powerup Panel',
            position=(150, 210),
            color=(0.1, 0.7, 1),  # Same as sandbox
            scale=1.0,
            h_align='center',
            v_align='center'
        )
        
        # Boxing Gloves Button
        bui.buttonwidget(
            parent=self._container,
            position=(30, 150),
            size=(240, 40),
            label='Get Permanent Gloves',
            button_type='square',
            color=self.colb,
            textcolor=self.wht,
            on_activate_call=self._give_boxing_gloves
        )
        
        # Triple Bombs Button
        bui.buttonwidget(
            parent=self._container,
            position=(30, 100),
            size=(240, 40),
            label='Get Triple Bombs',
            button_type='square',
            color=self.colb,
            textcolor=self.wht,
            on_activate_call=self._give_triple_bombs
        )
        
        # All Powerups Button
        bui.buttonwidget(
            parent=self._container,
            position=(30, 50),
            size=(240, 40),
            label='Get All Powerups',
            button_type='square',
            color=self.colb,
            textcolor=self.wht,
            on_activate_call=self._give_all_powerups
        )
    
    def _get_local_player_spaz(self):
        """Get the local player's spaz"""
        try:
            # Get the current activity
            activity = bs.get_foreground_host_activity()
            for player in activity.players:
                if player.sessionplayer.inputdevice.client_id == -1:  # Local player
                    actor = player.actor
                    if isinstance(actor, PlayerSpaz) and actor.node:
                        return actor
        except:
            pass
        return None
    
    def _give_boxing_gloves(self):
        """Give permanent boxing gloves to the local player"""
        spaz = self._get_local_player_spaz()
        if spaz:
            # Give boxing gloves and make them permanent
            spaz._has_boxing_gloves = True
            spaz.node.boxing_gloves = True
            push("You now have permanent boxing gloves!", color=(0, 1, 0))
        else:
            push("Could not find your character!", color=(1, 0, 0))
    
    def _give_triple_bombs(self):
        """Give triple bombs to the local player"""
        spaz = self._get_local_player_spaz()
        if spaz:
            spaz.set_bomb_count(3)  # Use the proper method
            spaz.bomb_type = 'normal'
            push("You now have triple bombs!", color=(0, 1, 0))
        else:
            push("Could not find your character!", color=(1, 0, 0))
    
    def _give_all_powerups(self):
        """Give all powerups to the local player"""
        spaz = self._get_local_player_spaz()
        if spaz:
            # Give all powerups
            spaz._has_boxing_gloves = True
            spaz.node.boxing_gloves = True
            spaz.set_bomb_count(3)
            spaz.bomb_type = 'normal'
            
            # Give shield
            if not spaz.shield:
                spaz._has_shield = True
                spaz.shield = bs.newnode('shield',
                                        owner=spaz.node,
                                        attrs={'color': (0.3, 0.3, 0.3),
                                               'radius': 1.3})
                spaz.node.connectattr('position_center', spaz.shield, 'position')
            
            # Full health
            spaz.node.hurt = 0.0
            
            push("All powerups granted!", color=(0, 1, 0))
        else:
            push("Could not find your character!", color=(1, 0, 0))


# ba_meta export babase.Plugin
class PowerupPlugin(babase.Plugin):
    def on_app_running(self):
        # Initialize the plugin
        NicePowerup()
