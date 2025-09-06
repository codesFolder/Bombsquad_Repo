# ba_meta require api 9
import babase
import bauiv1 as bui
import bauiv1lib.party
import random
import bascenev1 as bs
from bascenev1 import screenmessage as push

# --- Message Lists ---
# We've added messages with the {player} placeholder.
# The plugin will replace {player} with the name of your targeted player.
sorry_msgs = [
    "😅 Oops, my bad there!", "🙏 Sorry about that, {player}!",
    "🙇 My apologies, that was clumsy of me!", "😬 Whoops! Totally my fault.",
    "🙏 Sorry! I’ll make it up to you, {player}.", "😓 Didn’t mean to mess that up, sorry!",
    "🙁 My mistake, {player}, won’t happen again!", "🙇‍♂️ Apologies! That was on me."
]
gg_msgs = [
    "👏 Good game, everyone!", "🏆 GG! Well played, {player}. 👏",
    "🤝 Wooo — that was a solid match! 💪", "🎯 Nice game! You all played great.",
    "🏅 GG, {player}! Let’s do that again sometime.", "⚔️ Well fought, team! 💥",
    "🔥 GG! That was intense.", "🎮 Good game, {player}! Thanks for playing. 😊"
]
taunt_msgs = [
    "😏 Is that your best shot, {player}?", "😂 I’ve seen toddlers throw harder than that!",
    "🐌 {player}, that was so slow...", "⚠️ Careful, you might hurt yourself!",
    "🏆 If missing was a sport, you’d be champ.", "🙃 I almost felt that… almost.",
    "💨 You call that an attack, {player}?", "🎯 I’ve fought tougher opponents in the tutorial."
]


class PartyWindowWithButtons(bauiv1lib.party.PartyWindow):
    def __init__(s, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- NEW: Target selection variables ---
        s._target_players = []
        s._target_index = -1  # -1 means no one is targeted
        s._current_target_name = None
        # --- End of new variables ---

        # --- UI Customization Variables ---
        button_size = (50, 35)
        button_scale = 0.7
        start_pos_x = s._width - 60
        start_pos_y = s._height - 83
        horizontal_offset = 60
        # --- End of Customization ---

        s._cooldown_seconds = 5.0
        
        s._buttons_data = {
            'sorry': {
                'label': 'Sorry',
                'messages': sorry_msgs,
                'color': (1.0, 0.8, 0.3),  # Yellow
                'position': (start_pos_x - horizontal_offset, start_pos_y),
                'last_use_time': 0.0, 'widget': None
            },
            'gg': {
                'label': 'GG',
                'messages': gg_msgs,
                'color': (0.4, 1.0, 0.4),  # Green
                'position': (start_pos_x - (2 * horizontal_offset), start_pos_y),
                'last_use_time': 0.0, 'widget': None
            },
            'taunt': {
                'label': 'Taunt',
                'messages': taunt_msgs,
                'color': (1.0, 0.5, 0.3),  # Orange
                'position': (start_pos_x - (3 * horizontal_offset), start_pos_y),
                'last_use_time': 0.0, 'widget': None
            }
        }

        # Create the standard message buttons in a loop
        for name, data in s._buttons_data.items():
            data['widget'] = bui.buttonwidget(
                parent=s._root_widget,
                size=button_size,
                scale=button_scale,
                label=data['label'],
                color=data['color'],
                button_type='square',
                position=data['position'],
                on_activate_call=babase.Call(s._send_message, name)
            )

        # --- NEW: Create the Target Button ---
        s._btn_target = bui.buttonwidget(
            parent=s._root_widget,
            size=(80, 35), # Made it a bit wider to fit names
            scale=button_scale,
            label='Target',
            color=(0.6, 0.6, 0.8), # A purplish color
            button_type='square',
            position=(start_pos_x, start_pos_y), # Placed at the rightmost spot
            on_activate_call=s._cycle_target
        )

    def _cycle_target(s):
        """Finds players in the lobby and cycles through them as a target."""
        roster = bs.get_game_roster()
        # We want to target others, not ourselves.
        # So we get our own client ID to filter ourselves out.
        my_client_id = babase.app.classic.get_public_party_client_id()
        s._target_players = [
            p for p in roster if p['client_id'] != my_client_id
        ]

        if not s._target_players:
            push("No other players to target.")
            bui.getsound('error').play()
            s._current_target_name = None
            s._target_index = -1
            bui.buttonwidget(edit=s._btn_target, label='Target')
            return

        # Move to the next player in the list
        s._target_index += 1
        if s._target_index >= len(s._target_players):
            s._target_index = 0  # Loop back to the start

        target_player = s._target_players[s._target_index]
        s._current_target_name = target_player['display_string']
        
        # Update the button label to show who is targeted
        bui.buttonwidget(edit=s._btn_target, label=s._current_target_name)
        bui.getsound('tick').play()

    def _send_message(s, name: str):
        button_data = s._buttons_data[name]
        now = babase.apptime()
        
        # Cooldown check (unchanged)
        if now - button_data['last_use_time'] < s._cooldown_seconds:
            push("Too fast!")
            bui.getsound('error').play()
            return

        message_template = random.choice(button_data['messages'])

        # --- NEW: Player name replacement logic ---
        if '{player}' in message_template:
            if s._current_target_name:
                # If we have a target, replace the placeholder with their name
                final_message = message_template.replace('{player}', s._current_target_name)
            else:
                # If the message needs a target but we don't have one, abort.
                push("Select a target first!")
                bui.getsound('error').play()
                return
        else:
            # If the message doesn't have a placeholder, just use it as is.
            final_message = message_template

        bs.chatmessage(final_message)
        bui.getsound('swish').play()
        button_data['last_use_time'] = now
        s._update_cooldown_visual(name)

    def _update_cooldown_visual(s, name: str):
        # This function is unchanged
        button_data = s._buttons_data[name]
        if not button_data['widget'].exists():
            return
        now = babase.apptime()
        time_left = s._cooldown_seconds - (now - button_data['last_use_time'])
        if time_left > 0:
            bui.buttonwidget(edit=button_data['widget'], label=f'{time_left:.1f}')
            babase.apptimer(0.1, babase.Call(s._update_cooldown_visual, name))
        else:
            bui.buttonwidget(edit=button_data['widget'], label=button_data['label'])

# ba_meta export babase.Plugin
class byBordd(babase.Plugin):
    def __init__(s):
        bauiv1lib.party.PartyWindow = PartyWindowWithButtons
