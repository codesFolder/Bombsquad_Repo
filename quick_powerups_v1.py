# ba_meta require api 9
import babase
import _babase
import bauiv1 as bui
import bascenev1 as bs
from bascenev1 import broadcastmessage as push, get_foreground_host_activity as ga
from bauiv1lib.ingamemenu import InGameMenuWindow as igm
from bascenev1lib.actor.playerspaz import PlayerSpaz
from typing import Any, cast


class NicePowerup:
    """Main class similar to how sandbox.py uses Nice class"""
    
    # Define the same colors as sandbox
    cola = (0.13, 0.13, 0.13)
    colb = cola
    wht = (1, 1, 1)

    def __init__(self):
        # This is used to add the button to the in-game menu, following sandbox pattern
        pass

    def Button(self):
        """Create a button wrapper similar to sandbox.py's Button function"""
        def lmao(self):
            PowerupPanel()
            self._resume()

        def openBox(self):
            bui.buttonwidget(edit=self.sbox, icon=bui.gettexture('powerupPunchIcon'))
            bs.apptimer(0.6, bs.Call(closeBox, self))

        def closeBox(self):
            if self.sbox.exists():
                bui.buttonwidget(edit=self.sbox, icon=bui.gettexture('powerupPunchIcon'))

        def wrap(self=igm._refresh_in_game, *args, **kwargs):
            r = self(*args, **kwargs)
            # Add the powerup button to the in-game menu
            self.sbox = bui.buttonwidget(
                color=self.colb,
                parent=self._root_widget,
                position=(30, self._height - 110),  # Position similar to sandbox
                size=(100, 50),
                scale=1.0,
                textcolor=self.wht,
                label="Powerups",
                icon=bui.gettexture('powerupPunchIcon'),  # Use powerup icon
                iconscale=0.8,
                on_select_call=bs.Call(openBox, self),
                on_activate_call=bs.Call(lmao, self))
            return r
        return wrap


class PowerupPanel:
    """UI class to handle the powerup panel"""
    
    def __init__(self):
        # Use same colors as sandbox
        self.cola = NicePowerup.cola
        self.colb = NicePowerup.colb
        self.wht = NicePowerup.wht
        # Use same positioning and scaling as sandbox
        self.soff = (0, 0)
        self.howoff = 400
        self._pos = 0
        self._anim_out = 'out_right'
        self._anim_outv = 'out_left'
        self.anim_in = 'in_right'
        self.anim_inv = 'in_left'
        self.scale = 1.3
        self._height = 300
        self._width = 300
        self.center_pos = (0, 140)
        self._create_ui()
        
    def _create_ui(self):
        """Create the powerup panel UI following the sandbox.py structure"""
        # Get the overlay stack
        overlay_stack = bui.get_special_widget('overlay_stack')
        
        # Create the main container like in sandbox
        root_widget = self._rw = bui.containerwidget(
            parent=overlay_stack,
            size=(self._width, self._height),
            color=self.cola,  # Same as sandbox's cola color
            transition=self.anim_in,
            stack_offset=self.soff,
            scale=self.scale
        )
        
        # Title like in sandbox
        bui.textwidget(
            parent=root_widget,
            text='Powerup Panel',
            position=(120, 250),
            color=(0.1, 0.7, 1),  # Same as sandbox
            scale=1.0,
            h_align='center',
            v_align='center'
        )
        
        # Boxing Gloves Button
        bui.buttonwidget(
            parent=root_widget,
            position=(40, 185),
            size=(220, 50),
            label='Get Permanent Gloves',
            color=self.colb,
            textcolor=self.wht,
            button_type='square',
            on_activate_call=self._give_boxing_gloves
        )
        
        # Triple Bombs Button
        bui.buttonwidget(
            parent=root_widget,
            position=(40, 125),
            size=(220, 50),
            label='Get Triple Bombs',
            color=self.colb,
            textcolor=self.wht,
            button_type='square',
            on_activate_call=self._give_triple_bombs
        )
        
        # All Powerups Button
        bui.buttonwidget(
            parent=root_widget,
            position=(40, 65),
            size=(220, 50),
            label='Get All Powerups',
            color=self.colb,
            textcolor=self.wht,
            button_type='square',
            on_activate_call=self._give_all_powerups
        )

        # Back button
        bacc = bui.buttonwidget(
            parent=root_widget,
            size=(60, 20),
            label='Back',
            scale=self.scale,
            button_type='square',
            position=(40, 30),
            color=self.colb,
            textcolor=self.wht,
            on_activate_call=bs.Call(self.back))
        bui.containerwidget(edit=root_widget, cancel_button=bacc)

    def back(self, wosh=False):
        """Close the panel like in sandbox"""
        self.kill(wosh, self._rw)

    def kill(self, wosh=False, who=None, keep_hl=False, anim=True, rev=False):
        """Animate closing of the panel like in sandbox"""
        try:
            bui.containerwidget(edit=who, transition=(
                self._anim_out if not rev else self._anim_outv) if anim else None)
        except:
            pass
        if wosh:
            bui.getsound('swish').play()
    
    def _get_local_player_spaz(self):
        """Get the local player's spaz"""
        try:
            # Get the current activity
            activity = ga()
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
        # Apply the same pattern as sandbox to add button to in-game menu
        igm._refresh_in_game = NicePowerup().Button()(igm._refresh_in_game)
