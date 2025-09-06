# ba_meta require api 9
import babase
import bauiv1 as bui
import bauiv1lib.party
import random
import bascenev1 as bs
from bascenev1 import screenmessage as push
from bauiv1 import SpecialChar as sc

# --- Message Lists ---
# You can add or change any messages in these lists.

sorry_msgs = [
    "😅 Oops, my bad there!",
    "🙏 Sorry about that, didn’t mean to!",
    "🙇 My apologies, that was clumsy of me!",
    "😬 Whoops! Totally my fault.",
]

gg_msgs = [
    "👏 Good game, everyone! That was fun. 🎉",
    "🏆 GG! Well played all around. 👏",
    "🤝 Wooo — that was a solid match! 💪",
    "🎯 Nice game! You all played great. 🙌",
]

taunt_msgs = [
    "😏 Is that your best shot?",
    "😂 I’ve seen toddlers throw harder than that!",
    "🐌 That move was so slow, I had time to make a sandwich. 🥪",
    "⚠️ Careful, you might hurt yourself swinging like that!",
]

# New message lists (currently empty, you can fill them)
greet_msgs = [
    "Hey everyone! 👋",
    "Hello! Ready for a game? 😄",
    "Hi there! GLHF!",
    "Yo! Let's do this. 🔥",
]

bye_msgs = [
    "GG, gotta go. Bye! 👋",
    "That's all for me, see ya!",
    "Fun games! Catch you all later.",
    "I'm out, take care everyone!",
]

react_msgs = [
    "bruh",
    "wtf",
    "lol",
    "damn!",
    "oof",
    "💀",
]

# --- The Main Plugin Class ---

class PartyWindowWithButtons(bauiv1lib.party.PartyWindow):
    """
    A modified PartyWindow that adds a set of quick-chat buttons.
    """

    # --- CUSTOMIZATION VARIABLES ---
    # Edit these values to change the layout and appearance of the buttons.

    # 1. Button Cooldown
    COOLDOWN_SECONDS = 5.0  # Cooldown time in seconds for all buttons.

    # 2. Button Size and Scale
    BUTTON_SIZE = (45, 45)    # Width and height of the buttons.
    BUTTON_SCALE = 0.8       # How large the buttons appear.

    # 3. Button Layout and Position
    # The starting position for the FIRST button.
    # (0, 0) is the bottom-left corner of the window.
    START_POS = (10, 200)

    # The offset between each button. Change this to rearrange the layout.
    # Examples:
    # (50, 0)   -> Horizontal layout, from left to right.
    # (-50, 0)  -> Horizontal layout, from right to left.
    # (0, 50)   -> Vertical layout, from bottom to top.
    # (0, -50)  -> Vertical layout, from top to bottom.
    BUTTON_OFFSET = (0, 50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # This dictionary holds all the data and state for our buttons.
        # It's the core of the refactored code. Adding a new button is as
        # easy as adding a new entry here.
        self._buttons = {
            'greet': {
                'icon': sc.HAND,
                'color': (0.2, 0.6, 1.0),  # Blue
                'messages': greet_msgs,
                'last_use_time': 0.0,
                'widget': None
            },
            'sorry': {
                'icon': sc.FACE_SAD,
                'color': (1.0, 0.8, 0.3),  # Yellow
                'messages': sorry_msgs,
                'last_use_time': 0.0,
                'widget': None
            },
            'gg': {
                'icon': sc.TROPHY,
                'color': (0.4, 1.0, 0.4),  # Green
                'messages': gg_msgs,
                'last_use_time': 0.0,
                'widget': None
            },
            'taunt': {
                'icon': sc.FACE_FLAT,
                'color': (1.0, 0.5, 0.3),  # Orange
                'messages': taunt_msgs,
                'last_use_time': 0.0,
                'widget': None
            },
            'react': {
                'icon': sc.SHIELD,
                'color': (0.8, 0.5, 1.0),  # Purple
                'messages': react_msgs,
                'last_use_time': 0.0,
                'widget': None
            },
            'bye': {
                'icon': sc.DOOR,
                'color': (0.7, 0.7, 0.7),  # Gray
                'messages': bye_msgs,
                'last_use_time': 0.0,
                'widget': None
            },
        }

        # This loop creates all the buttons automatically based on our dictionary.
        for i, (name, data) in enumerate(self._buttons.items()):
            # Calculate the position for this button
            pos_x = self.START_POS[0] + i * self.BUTTON_OFFSET[0]
            pos_y = self.START_POS[1] + i * self.BUTTON_OFFSET[1]

            # Create the button widget
            data['widget'] = bui.buttonwidget(
                parent=self._root_widget,
                size=self.BUTTON_SIZE,
                scale=self.BUTTON_SCALE,
                label=bui.charstr(data['icon']),
                color=data['color'],
                button_type='square',
                position=(pos_x, pos_y),
                # This lambda function is important. It tells the button
                # to call our handler function with its unique name.
                on_activate_call=babase.Call(self._send_message, name)
            )

    def _send_message(self, name: str):
        """A single function to handle clicks for ALL buttons."""
        btn_data = self._buttons.get(name)
        if not btn_data:
            return

        # Check for cooldown
        now = babase.apptime()
        time_since_last_use = now - btn_data['last_use_time']

        if time_since_last_use < self.COOLDOWN_SECONDS:
            time_left = self.COOLDOWN_SECONDS - time_since_last_use
            push(f"Wait {time_left:.1f} more seconds!", color=(1, 0.5, 0))
            bui.getsound('error').play()
            return

        # If cooldown is over, send the message
        if not btn_data['messages']:
            push("No messages defined for this button!", color=(1, 0, 0))
            bui.getsound('error').play()
            return
            
        bs.chatmessage(random.choice(btn_data['messages']))
        bui.getsound('swish').play()

        # Update last use time and start the visual cooldown
        btn_data['last_use_time'] = now
        self._update_cooldown_visual(name)

    def _update_cooldown_visual(self, name: str):
        """Updates the button's label to show the cooldown timer."""
        btn_data = self._buttons.get(name)
        if not btn_data or not btn_data['widget'].exists():
            return

        now = babase.apptime()
        time_elapsed = now - btn_data['last_use_time']
        time_left = self.COOLDOWN_SECONDS - time_elapsed

        if time_left > 0:
            # If still in cooldown, show the remaining time
            bui.buttonwidget(edit=btn_data['widget'],
                             label=f'{time_left:.1f}')
            # Schedule this function to run again shortly
            babase.apptimer(0.1, babase.Call(self._update_cooldown_visual, name))
        else:
            # If cooldown is over, restore the original icon
            bui.buttonwidget(edit=btn_data['widget'],
                             label=bui.charstr(btn_data['icon']))


# ba_meta export babase.Plugin
class byBordd(babase.Plugin):
    def __init__(self):
        # This is the "monkey-patch" that replaces the original PartyWindow
        # with our new, modified version.
        bauiv1lib.party.PartyWindow = PartyWindowWithButtons
