from kivy import require
require('1.9.1')

from kivy.config import Config
Config.set('graphics', 'width', 370)
Config.set('graphics', 'height', 240)
Config.set('graphics', 'resizable', False)

import string, re, os
from datetime import datetime
import time
from functools import partial
from PIL import Image as _Image
from textwrap import TextWrapper

if not os.path.isdir('temp'):
    os.mkdir('temp')

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.uix.screenmanager import (Screen, ScreenManager,
                                    NoTransition, SlideTransition)
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.bubble import Bubble
from kivy.properties import (ListProperty, BooleanProperty,
                             StringProperty, ObjectProperty)
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import escape_markup
from kivy.uix.dropdown import DropDown
from kivy.uix.settings import Settings
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.clock import Clock
from kivy.graphics import Ellipse
from kivy.uix.image import Image
from kivy.base import stopTouchApp

Builder.load_string('''
<Label>:
    font_name: "fonts/OpenSans-Regular.ttf"
    halign: "center"
    color: 0, 0, 0, 1

<Button>:
    color: 1, 1, 1, 1
    disabled_color: 1, 1, 1, 1

<Popup>:
    size_hint: None, None
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    width: 250
    separator_height: 1
    title_font: "fonts/ionicons_semibold.ttf"

<ClockLabel>:
    text_size: self.size
    valign: 'bottom'
    color: 0.23, 0.23, 0.23, 1
    font_size: 8

<DateSpinner>:
    sync_height: True
    text_autoupdate: True

<DialogButton>:
    background_normal: 'textures/button/menu_bt_normal.png'
    background_down: 'textures/button/inputbt_down.png'
    background_disabled_normal: 'textures/button/menu_bt_normal.png'
    text_size: self.width - 10, self.height
    valign: 'center'
    font_size: 14
    font_name: 'fonts/ionicons_semibold.ttf'

<ErrorLabel>:
    text_size: self.size
    halign: "left"
    valign: "top"

<FramedScrollView>:
    canvas:
        Color:
            rgba: 0.23, 0.23, 0.23, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.86, 0.86, 0.86, 1
        Rectangle:
            pos: self.x + 1, self.y + 1
            size: self.width - 2, self.height - 2

<FullSizeButton>:
    text_size: self.width - self.bound[0], self.height - self.bound[1]

<FullSizeLabel>:
    text_size: self.width - self.bound[0], self.height - self.bound[1]

<HelpBar>:
    MenuButton:
        disabled: True
        size_hint: 0.33, 1
    MenuButton:
        text: " Help"
        size_hint: 0.27, 1
        background_normal: 'textures/button/inputbt_down.png'
        background_down: 'textures/button/menu_bt_normal.png'
        on_press: app.hide_screen(self, 'up')
    MenuButton:
        disabled: True

<HelpLabel>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Line:
            points: self.x, self.y + self.height, \
                    self.x + self.width, self.y + self.height, \
                    self.x + self.width, self.y, \
                    self.x, self.y, \
                    self.x, self.y + self.height
    markup: True
    font_size: 15
    text_size: self.size
    halign: "left"
    valign: "top"
    Image:
        source: 'textures/icons/python.png'
        size: 40, 40
        pos: 165, 285
    Image:
        source: 'textures/icons/kivy.png'
        size: 30, 30
        pos: 70, 265
    Image:
        source: 'textures/icons/ionic.png'
        size: 47, 47
        pos: 114, 214

#<InfoView>:
    #orientation: "vertical"
    #Label:
        #id: sent_text
        #markup: True
        #halign: "left"
        #text: root.sent_text
        #text_size: self.size
        #size_hint: 1, 0.4
        #font_size: 15
        #color: 1, 1, 1, 1

    #Label:
        #id: msg
        #text: "Message text:"
        #font_name: "fonts/OpenSans-Semibold.ttf"
        #size_hint: 1, 0.15
        #font_size: 13
        #color: 1, 1, 1, 1

    #TextInput:
        #id: msg_text
        #readonly: True
        #cursor_color: 0, 0, 0, 0
        #background_normal: "textures/textinput/msginput_unfocused.png"
        #background_active: "textures/textinput/msginput_unfocused.png"

<InputBox>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'textures/panels/input_panel.png'
    padding: 0, 8

<InputButton>:
    background_normal: 'textures/button/inputbt_normal.png'
    background_down: 'textures/button/inputbt_down.png'
    font_name: 'fonts/ionicons_semibold.ttf'

<LoggedAsLabel>:
    text_size: self.width - 10, self.height
    halign: "left"

<LoginLayout>:
    canvas.before:
        Color:
            rgba: 0.85, 0.92, 1, 1
        RoundedRectangle:
            pos: -28, 59
            size: 352, 42
        RoundedRectangle:
            pos: -28, 109
            size: 352, 42
        Color:
            rgba: 0.16, 0.36, 0.56, 1
        RoundedRectangle:
            pos: -27, 60
            size: 350, 40
        RoundedRectangle:
            pos: -27, 110
            size: 350, 40

<MenuAddBar>:
    canvas.before:
        Color:
            rgba: 0.86, 0.86, 0.86, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.16, 0.36, 0.56, 1
        Rectangle:
            pos: self.x, self.y + 1
            size: self.width, self.height - 2
    Widget:
        size_hint: 0.7, 1
    Button:
        id: add_bt
        text: "[size=20][/size] Add"
        size_hint: 0.3, 1
        markup: True
        font_name: 'fonts/ionicons_semibold.ttf'
        font_size: 17
        background_normal: 'textures/button/menu_bt_normal.png'
        background_down: 'textures/button/inputbt_down.png'

<MenuButton>:
    size_hint: 1, 0.09
    background_normal: 'textures/button/topbt_normal.png'
    background_down: 'textures/button/inputbt_down.png'
    font_name: 'fonts/ionicons_regular.ttf'
    font_size: 17
    markup: True

<MenuDivider>:
    canvas:
        Color:
            rgba: 0.86, 0.86, 0.86, 1
        Line:
            points: self.x, self.y, self.x, self.y + self.height
            width: 1.5
        Rectangle:
            source: 'textures/button/inputbt_normal.png'
            size: self.size
            pos: self.pos
        Line:
            points: self.x + self.width, self.y, self.x + self.width, self.y + self.height

<Message>:
    canvas:
        Color:
            rgba: 0.8, 0.8, 0.8, 1
        RoundedRectangle:
            pos: root.pos
            size: self.size
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            pos: root.x + 1, root.y + 1
            size: self.width - 2, self.height - 2

<MessageInput>:
    background_normal: 'textures/textinput/msginput_unfocused.png'
    background_active: 'textures/textinput/msginput_focused.png'
    font_name: "fonts/OpenSans-Regular.ttf"
    cursor_color: 0, 0, 0, 1
    write_tab: False

<MessageView>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    canvas.after:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        Line:
            points: self.x, self.y + self.height, \
                    self.x + self.width, self.y + self.height, \
                    self.x + self.width, self.y, \
                    self.x, self.y, \
                    self.x, self.y + self.height

<NickInput>:
    multiline: False
    font_size: 14
    font_name: "fonts/OpenSans-Regular.ttf"
    cursor_color: 0, 0, 0, 1
    write_tab: False
    background_normal: "textures/textinput/nickinput_unfocused.png"
    background_active: "textures/textinput/nickinput_focused.png"

<NickLabel>:
    background_color: 0, 0, 0, 0
    color: [0, 0, 0, 1] if self.state is 'normal' else [0.16, 0.36, 0.56, 1]
    size_hint_x: None
    width: self.texture_size[0]
    font_size: 13

<OptButton>:
    size_hint_y: None
    font_size: 12
    background_normal: 'textures/button/drop_opt.png'
    background_down: 'textures/button/drop_opt_down.png'
    height: 20

<PersonLayout>:
    canvas.after:
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Line:
            points: self.x, self.y + self.height, \
                    self.x + self.width, self.y + self.height, \
                    self.x + self.width, self.y, self.x, self.y, \
                    self.x, self.y + self.height

<PickerHead>:
    BoxLayout:
        size: root.size
        pos: root.pos
        Button:
            id: name
            size_hint: 0.8, 1
            text: "Select"
            color: 0, 0, 0, 1
            font_size: 11
            background_normal: "textures/button/picker_head.png"
            background_down: "textures/button/picker_head.png"
        Button:
            id: arrow
            size_hint: 0.2, 1
            background_normal: 'textures/button/arrow.png'
            background_down: 'textures/button/arrow_down.png'
            text: ""
            font_name: 'fonts/ionicons_semibold.ttf'
            font_size: 16

<Profile>:
    BoxLayout:
        orientation: "vertical"
        ProfileBar:
            size_hint: 1, 0.064
        ProfilePage:
            ProfileImage:
                id: avatar
                pos: 10, 360
                size: 100, 100
            ProfileField:
                id: nick
                pos: 120, 430
                font_size: 15
            ProfileLabel:
                pos: 120, 410
                text: "Status:"
            ProfileField:
                id: status
                pos: 120, 360
                height: 45
            ProfileLabel:
                pos: 10, 325
                text: "[size=18][/size] Email:"
            ProfileField:
                id: email
                pos: 120, 320
            ProfileLabel:
                pos: 10, 285
                text: "[size=18][/size] Birthday:"
            DatePicker:
                id: bday
                pos: 120, 280
                size_hint: None, None
                size: 220, 30
                disabled: not self.parent.editing
            ProfileLabel:
                pos: 10, 245
                text: "[size=18][/size] About:"
            ProfileField:
                id: about
                pos: 120, 115
                height: 150
            EditButton:
                id: edit
                text: " Edit"
                pos: 20, 10
            ProfileButton:
                id: delete
                text: " Delete"
                pos: 185, 10
                on_press: pass

<ProfileBar>:
    MenuButton:
        text: " Back"
        size_hint: 0.17, 1
        on_release: app.to_menu()
    MenuButton:
        disabled: True
        size_hint: 1, 1

<ProfileButton>:
    background_normal: 'textures/button/normal.png'
    background_down: 'textures/button/down.png'
    background_disabled_normal: 'textures/button/disabled.png'
    font_name: 'fonts/ionicons_semibold.ttf'
    size: 145, 40
    size_hint: None, None

<ProfileField>:
    size_hint: None, None
    size: 220, 30
    background_normal: "textures/textinput/msginput_unfocused.png"
    cursor_color: [0, 0, 0, 1] if self.parent.editing else [0, 0, 0, 0]
    background_color: [1, 1, 1, 1] if self.parent.editing else [0, 0, 0, 0]
    selection_color: [0.1843, 0.6549, 0.8313, 0.5] if self.parent.editing else [0, 0, 0, 0]
    readonly: not self.parent.editing
    font_size: 13

<ProfileImage@BoxLayout>:
    padding: 3
    size_hint: None, None
    canvas.before:
        Color:
            rgba: 0.85, 0.92, 1, 1
        Rectangle:
            size: root.size
            pos: root.pos
        Color:
            rgba: 0.16, 0.36, 0.56, 1
        Rectangle:
            size: root.width - 2, root.height - 2
            pos: root.x + 1, root.y + 1
    Image:
        id: src

<ProfileLabel@Label>:
    size_hint: None, None
    size: 80, 20
    text_size: self.size
    halign: "left"
    font_size: 12
    markup: True

<RecordDivider>:
    height: 15
    color: 1, 1, 1, 1
    font_size: 12
    text_size: self.width - 10, self.height
    halign: 'left'
    size_hint: 1, None
    canvas.before:
        Color:
            rgba: 0.86, 0.86, 0.86, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.23, 0.23, 0.23, 1
        Rectangle:
            pos: self.x + 1, self.y + 1
            size: self.width - 2, self.height - 2

<RegLabel>:
    color: 1, 1, 1, 1
    font_name: 'fonts/ionicons_semibold.ttf'
    size_hint: 0.7, 1
    text_size: self.width - 20, self.height - 10
    halign: "left"
    valign: "center"
    canvas.before:
        Color:
            rgba: 0.86, 0.86, 0.86, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.16, 0.36, 0.56, 1
        Rectangle:
            pos: self.x, self.y + 1
            size: self.width, self.height - 2

<RegisterLayout>:
    canvas.before:
        Color:
            rgba: 0.85, 0.92, 1, 1
        RoundedRectangle:
            pos: -28, 52
            size: 352, 45
        RoundedRectangle:
            pos: -28, 102
            size: 352, 45
        RoundedRectangle:
            pos: -28, 153
            size: 352, 45
        Color:
            rgba: 0.16, 0.36, 0.56, 1
        RoundedRectangle:
            pos: -27, 53
            size: 350, 43
        RoundedRectangle:
            pos: -27, 103
            size: 350, 43
        RoundedRectangle:
            pos: -27, 154
            size: 350, 43

<SmileBubble>:
    canvas:
        Color:
            rgba: 0.16, 0.36, 0.56, 0.7
        RoundedRectangle:
            pos: self.x, self.y + 10
            size: self.width, self.height - 10
    size_hint: None, None
    show_arrow: False
    pos: 170, 95
    size: 175, 275
    background_color: 0, 0, 0, 0
    GridLayout:
        id: smile_grid
        cols: 5

<SpinnerOption>:
    background_normal: 'textures/button/normal.png'
    background_down: 'textures/button/down.png'

<UsernameButton>:
    text_size: self.width - 10, self.height
    halign: 'left'
    valign: 'center'
    font_size: 13

<UserRecord>:
    canvas:
        Color:
            rgba: 0.16, 0.36, 0.56, 1
        Line:
            points: self.x, self.y, \
                    self.x + self.width, self.y, \
                    self.x + self.width, self.y + self.height, \
                    self.x, self.y + self.height, \
                    self.x, self.y
        Color:
            rgba: 0.16, 0.36, 0.56, 0.3
        Rectangle:
            pos: self.pos
            size: self.size

<YesNoButton>:
    background_normal: 'textures/button/normal.png'
    background_down: 'textures/button/down.png'
    background_disabled_normal: 'textures/button/disabled.png'
    font_name: 'fonts/ionicons_semibold.ttf'
''')


class SmileButton(Button):
    def on_press(self):
        self.color = (0.6, 0.8, 1, 1)

    def on_release(self):
        self.color = (1, 1, 1, 1)


class ClockLabel(Label):
    def __init__(self, tm, **kwargs):
        super().__init__(**kwargs)
        self.text = datetime.fromtimestamp(tm // 100).strftime("%H:%M")


class Message(BoxLayout):
    bg_color = ListProperty([0.99, 0.99, 0.99, 1])
    tw = TextWrapper(width = 20)
    sent = ('Sender: [color=#B6DAFF]{}[/color]'
            '\nTime: [color=#C8C8C8]{}[/color]')

    def width_modify(self):
        min_width = 160
        max_width = 320
        max_line = max(self.text_box._lines_labels,
                       key = lambda x: x.width).width
        curr_width = max_line + 15
        if curr_width < min_width:
            return min_width
        elif curr_width > max_width:
            return max_width
        else:
            return curr_width

    def line_wrap(self, text):
        spl = re.split('(\n{2,})', text)
        res = ''
        for idx, part in enumerate(spl):
            res += part if idx % 2 else self.tw.fill(part)
        return res

    def __init__(self, text, tm, sender, scr, **kwargs):
        super().__init__(**kwargs)
        self.text_box = TextInput(font_name = "fonts/OpenSans-Regular.ttf",
                                  font_size = 13,
                                  background_color = (0, 0, 0, 0),
                                  readonly = True,
                                  cursor_color = (0, 0, 0, 0))

        self.real_text = text
        self.text_box.text = self.line_wrap(text)
        self.sender = sender
        self.time = tm
        self.scr = scr

        self.height = (self.text_box.text.count('\n') + 2) * 19
        self.add_widget(self.text_box)

        if sender != app.nick:
            self.bg_color = [0.91, 0.95, 1, 1]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            info_popup = self.scr.info_popup
            sent_text = self.sent.format(self.sender,
                                         datetime.fromtimestamp(self.time // 100).strftime("%H:%M:%S"))
            info_popup.info_view.info_lb.text = sent_text
            info_popup.info_view.msg_text.text = self.real_text
            info_popup.open()


class SmileBubble(Bubble):
    hidden = BooleanProperty(True)


class NickInput(TextInput):
    checker = ObjectProperty()
    def on_text(self, inst, text):
        self.checker.check_next()
        if len(text) > 15:
            self.text = text[:15]


class MessageView(ScrollView):
    pass


class PersonLayout(FloatLayout):
    pass


class RegLabel(Label):
    pass


class RegisterLayout(BoxLayout):
    pass


class LoginLayout(BoxLayout):
    pass


class ChatPicker(DropDown):
    def __init__(self, **kwargs):
        self.selected = False
        super().__init__(**kwargs)

    def on_select(self, name):
        app.drop_mnt.ids['name'].text = name
        self.selected = True
        app.check_next()


class PickerHead(Widget):
    def on_release(self):
        app.drop_picker.open()


class Status(BoxLayout):
    online = BooleanProperty(True)
    def __init__(self, online = True, **kwargs):
        super().__init__(**kwargs)
        self.img = Image(source = 'textures/panels/status_on.png')
        self.online = online
        self.add_widget(self.img)

    def on_online(self, inst, ch):
        path = 'textures/panels/status_' + ('on.png' if ch else 'off.png')
        self.img.source = path


class NickLabel(Button):
    pass


class InfoView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.info_lb = FullSizeLabel(markup = True,
                                       halign = 'left',
                                       bound = [0, 0],
                                       size_hint = (1, 0.4),
                                       font_size = 15,
                                       color = (1, 1, 1, 1))

        self.msg_label = Label(text = "Message text:",
                               font_name = "fonts/OpenSans-Semibold.ttf",
                               size_hint = (1, 0.15),
                               font_size = 13,
                               color = (1, 1, 1, 1))

        self.msg_text = TextInput(readonly = True,
                                  cursor_color = (0, 0, 0, 0),
                                  background_normal = "textures/textinput/"
                                                      "msginput_unfocused.png",
                                  background_active = "textures/textinput/"
                                                      "msginput_unfocused.png")

        self.add_widget(self.info_lb)
        self.add_widget(self.msg_label)
        self.add_widget(self.msg_text)



class ChatTopBar(BoxLayout):
    pass


class HelpBar(BoxLayout):
    pass


class ProfileBar(BoxLayout):
    pass


class Profile(Screen):
    pass


class ProfileField(TextInput):
    pass


class ProfileButton(Button):
    pass


class YesNoButton(Button):
    pass


class EditButton(ToggleButton, ProfileButton):
    def nick_sync(self):
        app = app
        new = app.my_profile.ids['nick'].text
        if app.nick != new:
            app.my_name.text = new
            for i in app.msg_stack:
                if i.sender == app.nick:
                    i.sender = new
            app.nick = new

    def on_state(self, bt, state):
        if state == 'down':
            self.parent.editing = not self.parent.editing
        else:
            self.nick_sync()
            self.parent.editing = not self.parent.editing


class ProfilePage(FloatLayout):
    editing = BooleanProperty(False)
    def edit(self, bt):
        editing = not editing


class PersonProfile(Profile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids['edit'].disabled = True
        self.ids['delete'].disabled = True
        self.ids['status'].text = "Making your messages uppercase since 2016"
        self.ids['email'].text = "UNDEFINED"
        self.ids['about'].text = "I'm just a bot"


class SelfProfile(Profile):
    pass


class MessageInput(TextInput):
    def __init__(self, plch, **kwargs):
        self.placeholder = plch
        self.hint_text = self.placeholder
        super().__init__(**kwargs)

    def on_focus(self, inst, focus):
        self.hint_text = '' if focus or self.text else self.placeholder


class InputBox(BoxLayout):
    pass


class InputButton(Button):
    pass


class DateSpinnerItem(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 12
        self.background_normal = 'textures/button/drop_opt.png'
        self.background_down = 'textures/button/drop_opt_down.png'


class DateSpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.option_cls = DateSpinnerItem
        #self.background_normal = ''
        self.background_normal = 'textures/button/inputbt_down.png'
        self.background_color = (0, 0, 0, 0)

    def on_is_open(self, inst, state):
        super().on_is_open(inst, state)
        inst.background_color = ((1, 1, 1, 1) if state else (0, 0, 0, 0))


class DateTextField(TextInput):
    def __init__(self, prev, **kwargs):
        self.text_limit = len(prev)
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.font_size = 11
        self.foreground_color = (1, 1, 1, 1)
        self.cursor_color = (0, 0, 0, 1)
        self.multiline = False
        self.write_tab = False
        self.prev = prev
        self.text = prev

    def on_focus(self, inst, state):
        if state:
            inst.prev = inst.text
            inst.text = ''
        self.background_color = (1, 1, 1, 1) if state else (0, 0, 0, 0)
        self.foreground_color = (0, 0, 0, 1) if state else (1, 1, 1, 1)
        if not state:
            self.parent.update_date(self)

    def on_text(self, inst, text):
        if not text.isdigit():
            inst.text = text[:-1]
        if len(text) > self.text_limit:
            inst.text = text[:self.text_limit]

    def on_text_validate(self):
        self.text = self.text.zfill(self.text_limit)


class DatePickerDelim(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.01, 1)
        self.color = (1, 1, 1, 1)
        self.font_size = 13


class DatePicker(BoxLayout):
    month_match = {'January':   1,
                   'February':  2,
                   'March':     3,
                   'April':     4,
                   'May':       5,
                   'June':      6,
                   'July':      7,
                   'August':    8,
                   'September': 9,
                   'October':  10,
                   'November': 11,
                   'December': 12}

    def update_date(self, inst, tx = None):
        try:
            ts = datetime(int(self.year.text),
                          self.month_match[self.month.text],
                          int(self.day.text))
            self.timestamp = ts.timestamp()
        except (ValueError, OverflowError):
            inst.text = inst.default
            ErrorDisp("You've entered an invalid date. Try again").open()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = 0
        curr_year = datetime.now().year

        self.year = DateTextField(size_hint = (0.3, 1),
                                  prev = '1970')

        self.month = DateSpinner(size_hint = (0.5, 1),
                                 font_size = 12,
                                 values = ('January', 'February', 'March', 'April',
                                           'May', 'June', 'July', 'August', 'September',
                                           'October', 'November', 'December'))

        self.day = DateTextField(size_hint = (0.2, 1),
                                 prev = '01')

        self.month.bind(text = self.update_date)

        self.add_widget(self.day)
        self.add_widget(self.month)
        self.add_widget(self.year)


class ExtendedDatePicker(DatePicker):
    def update_date(self, inst = None, text = None):
            try:
                ts = datetime(int(self.year.text),
                              self.month_match[self.month.text],
                              int(self.day.text),
                              hour = int(self.hour.text),
                              minute = int(self.minute.text),
                              second = int(self.second.text))
                self.timestamp = ts.timestamp()
            except (ValueError, OverflowError):
                inst.text = inst.prev

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hour = DateTextField(size_hint = (0.2, 1),
                                  prev = '00')
        self.minute = DateTextField(size_hint = (0.2, 1),
                                    prev = '00')
        self.second = DateTextField(size_hint = (0.2, 1),
                                    prev = '00')

        self.add_widget(DatePickerDelim())
        self.add_widget(self.hour)
        self.add_widget(DatePickerDelim(text=':'))
        self.add_widget(self.minute)
        self.add_widget(DatePickerDelim(text=':'))
        self.add_widget(self.second)


class HelpLabel(Label):
    def __init__(self, **kwargs):
        text = """"""
        self.text = text
        super().__init__(**kwargs)


class ShowPswdButton(ToggleButton):
    def on_state(self, bt, value):
        self.parent.toggle_psw(value)


class RegScreen(Screen):
    def check_next(self):
        usr = self.tx_usr.text
        psw = self.tx_pass.text
        con = self.tx_con.text
        self.bt_next.disabled = not (usr and psw and psw == con)

    def toggle_psw(self, state):
        if state == 'down':
            self.show_psw.text = ' Hide password'
            self.tx_pass.password = False
            self.tx_con.password = False
        else:
            self.show_psw.text = ' Show password'
            self.tx_pass.password = True
            self.tx_con.password = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_box = RegisterLayout(size_hint = (1, 0.12),
                                      pos_hint = {"top": 1})

        self.lb_reg = RegLabel(text = "Register")

        self.to_login = InputButton(size_hint = (0.25, 1),
                                    font_name = "fonts/ionicons_regular.ttf",
                                    text = " Login",
                                    on_release = app.to_login,
                                    background_normal = 'textures/button/menu_bt_normal.png')

        self.lb_usr = Label(size_hint = (0.28, 0.03),
                            pos_hint = {"top": 0.75, "right": 0.255},
                            text = "Username",
                            color = (1, 1, 1, 1),
                            font_size = 16)

        self.tx_usr = NickInput(size_hint = (0.6, 0.13),
                                pos_hint = {"top": 0.795, "right": 0.85},
                                checker = self)

        self.lb_pass = Label(size_hint = (0.28, 0.03),
                             pos_hint = {"top": 0.54, "right": 0.25},
                             text = "Password",
                             color = (1, 1, 1, 1),
                             font_size = 16)

        self.tx_pass = NickInput(size_hint = (0.6, 0.13),
                                 pos_hint = {"top": 0.585, "right": 0.85},
                                 password = True,
                                 checker = self)

        self.lb_con = Label(size_hint = (0.28, 0.03),
                            pos_hint = {"top": 0.33, "right": 0.235},
                            text = "Confirm",
                            color = (1, 1, 1, 1),
                            font_size = 16)

        self.tx_con = NickInput(size_hint = (0.6, 0.13),
                                pos_hint = {"top": 0.375, "right": 0.85},
                                password = True,
                                checker = self)

        self.bt_next = Button(size_hint = (0.4, 0.15),
                              pos_hint = {"top": 0.14, "right": 0.94},
                              text = "Next",
                              font_size = 16,
                              disabled = True,
                              background_normal = "textures/button/normal_intro.png",
                              background_down = "textures/button/down_intro.png",
                              background_disabled_normal = "textures/button/disabled_intro.png",
                              on_release = app.register)

        self.show_psw = ShowPswdButton(size_hint = (0.4, 0.15),
                                       pos_hint = {"top": 0.16, "right": 0.4},
                                       text = ' Show password',
                                       font_name = "fonts/ionicons_regular.ttf",
                                       background_color = (0, 0, 0, 0))

        self.add_widget(self.top_box)

        self.top_box.add_widget(self.lb_reg)
        self.top_box.add_widget(self.to_login)
        self.add_widget(self.lb_usr)
        self.add_widget(self.tx_usr)
        self.add_widget(self.lb_pass)
        self.add_widget(self.tx_pass)
        self.add_widget(self.lb_con)
        self.add_widget(self.tx_con)
        self.add_widget(self.bt_next)
        self.add_widget(self.show_psw)


class ErrorLabel(Label):
    pass


class ErrorDisp(Popup):
    def __init__(self, text, **kwargs):
        self.cont = FloatLayout()
        self.btn = Button(size_hint = (0.4, 0.2),
                     pos_hint = {"top": 0.163, "right": 0.94},
                     text = "Back",
                     font_size = 15,
                     background_normal = "textures/button/normal_intro.png",
                     background_down = "textures/button/down_intro.png",
                     on_release = self.dismiss)
        self.lb = ErrorLabel(text = text,
                        font_size = 13,
                        color = (1, 1, 1, 1),
                        size_hint = (0.95, 0.8),
                        pos_hint = {"top": 0.99, "center_x": 0.5},
                        halign = "left",
                        valign = "top")

        self.cont.add_widget(self.lb)
        self.cont.add_widget(self.btn)
        super().__init__(title = 'Error',
                         content = self.cont,
                         height = 180,
                         **kwargs)


class MenuButton(Button):
    def __init__(self, **kwargs):
        if 'text' in kwargs and 'num' in kwargs:
            text_t = kwargs.pop('text')
            num = kwargs.pop('num')
            self.text = ('[size=24]' + text_t[0] + '[/size]' +
                         ' ' * num[0] + text_t[1] + ' ' * num[1])
        super().__init__(**kwargs)


class MenuDivider(Widget):
    pass


class RecordDivider(Label):
    pass


class LoggedAsLabel(Label):
    pass


class MenuAddBar(BoxLayout):
    pass


class UsernameButton(Button):
    pass


class FullSizeButton(Button):
    bound = ListProperty([0, 0])


class FullSizeLabel(Label):
    bound = ListProperty([0, 0])


class YesNoDialog(Popup):
    def ch_yes(self, bt):
        pass

    def ch_no(self, bt):
        pass

    def __init__(self, title, question):
        box = BoxLayout(orientation = "vertical")
        self.height = 155
        self.title = title
        self.title_size = 16

        question_lb = Label(size_hint = (1, 0.6),
                            text = question,
                            color = (1, 1, 1, 1),
                            font_name = "fonts/ionicons_semibold.ttf")

        answers = BoxLayout(size_hint = (1, 0.4),
                                 spacing = 4,
                                 padding = 2)
        yes = YesNoButton(text = " Yes",
                          on_release = self.ch_yes)

        no = YesNoButton(text = " No",
                         on_release = self.ch_no)

        box.add_widget(question_lb)
        box.add_widget(answers)

        answers.add_widget(yes)
        answers.add_widget(no)

        self.content = box
        super().__init__()


class LogoutDialog(YesNoDialog):
    def __init__(self):
        super().__init__(" Log out",
                         "Do you want to log out?")

    def ch_yes(self, bt):
        self.dismiss()
        Clock.schedule_once(app.logout, 0.15)

    def ch_no(self, bt):
        self.dismiss()


class QuitDialog(YesNoDialog):
    def __init__(self):
        super().__init__(" Quit",
                         "Do you want to quit?")

    def ch_yes(self, bt):
        self.dismiss()
        stopTouchApp()

    def ch_no(self, bt):
        self.dismiss()


class InfoBox(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.avatar = Ellipse(size = (105, 105),
                                  pos = (5, 250))
        self.logged_as_lb = LoggedAsLabel(size_hint = (1, 0.25),
                                          pos_hint = {"top": 1},
                                          font_size = 13)
        self.add_widget(self.logged_as_lb)


class MenuScreen(Screen):
    def build_usr_list(self, users):
        self.users_disp.clear_widgets()

        add = self.users_disp.add_widget
        add(self.div_favs)
        for online, name in users[0]:
            add(FavRecord(online, name))
        add(self.div_requests)
        for online, name in users[1]:
            add(RequestGotRecord(online, name))
        add(self.div_online)
        for online, name in users[2]:
            add(FriendRecord(online, name))
        add(self.div_offline)
        for online, name in users[3]:
            add(FriendRecord(online, name))
        add(self.div_req_sent)
        for online, name in users[4]:
            add(RequestSentRecord(online, name))
        add(self.div_blacklist)
        for online, name in users[5]:
            add(BlacklistRecord(online, name))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = BoxLayout()
        self.left_bar = BoxLayout(size_hint = (0.4, 1),
                                  orientation = "vertical")
        self.right_bar = BoxLayout(size_hint = (0.6, 1),
                                   orientation = "vertical")
        self.divider = MenuDivider(size_hint = (0.01, 1))

        self.menu_label = RegLabel(text = "Menu",
                                   size_hint = (1, 0.08),
                                   font_size = 17)

        self.info_box = InfoBox(size_hint = (1, 0.3))

        self.profile_bt = MenuButton(text = ('', "Profile"),
                                     num = (14, 14),
                                     on_release = app.to_self_profile)

        self.logout_dlg = LogoutDialog()
        self.logout_bt = MenuButton(text = ('', 'Log out'),
                                    num = (13, 13),
                                    on_release = self.logout_dlg.open)

        self.settings_bt = MenuButton(text = ('', 'Settings'),
                                      num = (12, 13),
                                      on_release = app.to_settings)

        self.help_bt = MenuButton(text = ('', 'Help'),
                                  num = (15, 16),
                                  on_release = app.to_help)

        self.quit_dlg = QuitDialog()
        self.quit_bt = MenuButton(text = ('', 'Quit'),
                                  num = (16, 16),
                                  on_release = self.quit_dlg.open)

        self.add_bar = MenuAddBar(size_hint = (1, 0.105))

        self.disp_scroll = ScrollView(bar_inactive_color = (0, 0, 0, 0),
                                      bar_color = (0.3, 0.3, 0.3, 0.7),
                                      bar_margin = 3,
                                      do_scroll_x = False,
                                      size_hint = (1, 1))
        self.users_disp = GridLayout(cols = 1,
                                     size_hint_y = None)
        self.users_disp.bind(minimum_height = self.users_disp.setter('height'))

        self.add_button = self.add_bar.ids['add_bt']
        self.add_person_popup = AddPersonPopup()
        self.add_button.on_press = self.add_person_popup.open

        self.div_favs = RecordDivider(text = "favorites")
        self.div_requests = RecordDivider(text = "add requests")
        self.div_online = RecordDivider(text = "online")
        self.div_offline = RecordDivider(text = "offline")
        self.div_req_sent = RecordDivider(text = "request sent")
        self.div_blacklist = RecordDivider(text = "blacklist")

        self.add_widget(self.container)

        self.container.add_widget(self.left_bar)
        self.container.add_widget(self.divider)
        self.container.add_widget(self.right_bar)

        self.left_bar.add_widget(self.menu_label)
        self.left_bar.add_widget(self.info_box)
        self.left_bar.add_widget(self.profile_bt)
        self.left_bar.add_widget(self.logout_bt)
        self.left_bar.add_widget(self.settings_bt)
        self.left_bar.add_widget(self.help_bt)
        self.left_bar.add_widget(self.quit_bt)

        self.right_bar.add_widget(self.add_bar)
        self.right_bar.add_widget(self.disp_scroll)
        self.disp_scroll.add_widget(self.users_disp)


class UserRecord(BoxLayout):
    def f_to_profile(self, bt):
        self.opts.dismiss()
        nick = bt.record.name.text
        app.to_profile(nick)

    def f_remove_favs(self, bt):
        self.opts.dismiss()
        app.remove_favs()

    def f_remove_friends(self, bt):
        self.opts.dismiss()
        app.remove_friends()

    def f_add_bl(self, bt):
        self.opts.dismiss()
        app.add_bl()

    def f_add_favs(self, bt):
        self.opts.dismiss()
        app.add_favs()

    def f_get_request_msg(self, bt):
        self.opts.dismiss()
        app.get_request_msg()

    def f_accept_request(self, bt):
        self.opts.dismiss()
        app.accept_request()

    def f_decline_request(self, bt):
        self.opts.dismiss()
        app.decline_request()

    def f_take_request_back(self, bt):
        self.opts.dismiss()
        app.take_request_back()

    def f_remove_bl(self, bt):
        self.opts.dismiss()
        app.remove_bl()

    def more_action(self, bt):
        self.opts.open(self)

    def __init__(self, name, online, **kwargs):
        super().__init__(**kwargs)
        self.status = Status(online = online,
                             size_hint = (0.08, 1))
        self.name = UsernameButton(text = name,
                                   size_hint = (0.79, 1),
                                   background_color = (0, 0, 0, 0),
                                   color = (0, 0, 0, 1),
                                   on_press = app.to_dialog)
        self.opts = DropDown()

        self.more = FullSizeButton(text = '',
                                   halign = 'right',
                                   font_name = 'fonts/ionicons_regular.ttf',
                                   font_size = 25,
                                   bound = [20, 0],
                                   color = (0, 0, 0, 1),
                                   size_hint = (0.13, 1),
                                   background_color = (0, 0, 0, 0),
                                   on_release = self.more_action)
        self.size_hint = [1, None]
        self.height = 30

        self.add_widget(self.status)
        self.add_widget(self.name)
        self.add_widget(self.more)


class OptButton(Button):
    def __init__(self, record, **kwargs):
        self.record = record
        super().__init__(**kwargs)


class FavRecord(UserRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = OptButton(self,
                                 text = "Profile",
                                 on_press = self.f_to_profile)
        self.remove_favs = OptButton(self,
                                     text = "Remove from favorites",
                                     on_press = self.f_remove_favs)
        self.remove_friends = OptButton(self,
                                        text = "Remove from friends",
                                        on_press = self.f_remove_friends)
        self.add_bl = OptButton(self,
                                text = "Add to blacklist",
                                on_press = self.f_add_bl)

        self.opts.add_widget(self.profile)
        self.opts.add_widget(self.remove_favs)
        self.opts.add_widget(self.remove_friends)
        self.opts.add_widget(self.add_bl)


class FriendRecord(UserRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = OptButton(self,
                                 text = "Profile",
                                 on_press = self.f_to_profile)
        self.add_favs = OptButton(self,
                                  text = "Add to favorites",
                                  on_press = self.f_add_favs)
        self.remove_friends = OptButton(self,
                                        text = "Remove from friends",
                                        on_press = self.f_remove_friends)
        self.add_bl = OptButton(self,
                                text = "Add to blacklist",
                                on_press = self.f_add_bl)

        self.opts.add_widget(self.profile)
        self.opts.add_widget(self.add_favs)
        self.opts.add_widget(self.remove_friends)
        self.opts.add_widget(self.add_bl)


class RequestGotRecord(UserRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = OptButton(self,
                                 text = "Profile",
                                 on_press = self.f_to_profile)
        self.request_msg = OptButton(self,
                                     text = "Request message",
                                     on_press = self.f_get_request_msg)
        self.accept = OptButton(self,
                                text = "Accept",
                                on_press = self.f_accept_request)
        self.decline = OptButton(self,
                                 text = "Decline",
                                 on_press = self.f_decline_request)

        self.opts.add_widget(self.profile)
        self.opts.add_widget(self.request_msg)
        self.opts.add_widget(self.accept)
        self.opts.add_widget(self.decline)


class RequestSentRecord(UserRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.take_back = OptButton(self,
                                   text = "Take back",
                                   on_press = self.f_take_request_back)

        self.opts.add_widget(self.take_back)


class BlacklistRecord(UserRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = OptButton(self,
                                 text = "Profile",
                                 on_press = self.f_to_profile)
        self.remove_bl = OptButton(self,
                                   text = "Remove from blacklist",
                                   on_press = self.f_remove_bl)

        self.opts.add_widget(self.profile)
        self.opts.add_widget(self.remove_bl)


class SearchRecord(UserRecord):
    def f_to_profile(self, bt):
        self.opts.dismiss()
        nick = bt.record.name.text
        app.to_profile(nick, from_search = True)

    def f_ask_msg(self, bt):
        self.opts.dismiss()
        self.popup.dismiss()
        self.popup.msg_popup.open()

    def f_send_request(self, bt = None):
        # msg = self.popup.msg_input.text
        # name = self.name.text
        # make sure to clean the msg field
        self.popup.msg_popup.dismiss()
        app.send_request()

    def __init__(self, popup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.popup = popup
        self.popup.msg_confirm.on_release = self.f_send_request
        self.profile = OptButton(self,
                                 text = "Profile",
                                 on_press = self.f_to_profile)
        self.send_req = OptButton(self,
                                   text = "Send add request",
                                   on_press = self.f_ask_msg)

        self.opts.add_widget(self.profile)
        self.opts.add_widget(self.send_req)


class LoginScreen(Screen):
    def check_next(self):
        usr = self.tx_usr.text
        psw = self.tx_pass.text
        self.bt_next.disabled = not (usr and psw)

    def toggle_psw(self, state):
        if state == 'down':
            self.show_psw.text = ' Hide password'
            self.tx_pass.password = False
        else:
            self.show_psw.text = ' Show password'
            self.tx_pass.password = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_box = LoginLayout(size_hint = (1, 0.145),
                                   pos_hint = {"top": 1})

        self.lb_log = RegLabel(text = "Login")

        self.to_register = InputButton(size_hint = (0.25, 1),
                                       font_name = "fonts/ionicons_regular.ttf",
                                       text = "[size=18][/size] Register",
                                       markup = True,
                                       on_release = app.to_register,
                                       background_normal = 'textures/button/menu_bt_normal.png')

        self.lb_usr = Label(size_hint = (0.28, 0.03),
                            pos_hint = {"top": 0.67, "right": 0.255},
                            text = "Username",
                            color = (1, 1, 1, 1),
                            font_size = 16)

        self.tx_usr = NickInput(size_hint = (0.6, 0.15),
                                pos_hint = {"top": 0.73, "right": 0.85},
                                checker = self)

        self.lb_pass = Label(size_hint = (0.28, 0.03),
                             pos_hint = {"top": 0.42, "right": 0.25},
                             text = "Password",
                             color = (1, 1, 1, 1),
                             font_size = 16)

        self.tx_pass = NickInput(size_hint = (0.6, 0.15),
                                 pos_hint = {"top": 0.475, "right": 0.85},
                                 password = True,
                                 checker = self)

        self.bt_next = Button(size_hint = (0.4, 0.18),
                              pos_hint = {"top": 0.165, "right": 0.94},
                              text = "Next",
                              font_size = 16,
                              disabled = True,
                              background_normal = "textures/button/normal_intro.png",
                              background_down = "textures/button/down_intro.png",
                              background_disabled_normal = "textures/button/disabled_intro.png",
                              on_release = app.login)

        self.show_psw = ShowPswdButton(size_hint = (0.4, 0.15),
                                       pos_hint = {"top": 0.16, "right": 0.4},
                                       text = ' Show password',
                                       font_name = "fonts/ionicons_regular.ttf",
                                       background_color = (0, 0, 0, 0))

        self.add_widget(self.top_box)

        self.top_box.add_widget(self.lb_log)
        self.top_box.add_widget(self.to_register)
        self.add_widget(self.lb_usr)
        self.add_widget(self.tx_usr)
        self.add_widget(self.lb_pass)
        self.add_widget(self.tx_pass)
        self.add_widget(self.bt_next)
        self.add_widget(self.show_psw)


class FramedScrollView(ScrollView):
    pass


class SearchInput(MessageInput):
    def __init__(self, cont, plch, **kwargs):
        super().__init__(plch, **kwargs)
        self.cont = cont

    def on_text(self, inst, text):
        if len(text) > 15:
            self.text = text[:15]
        inst.cont.update_result(text)


class AddPersonPopup(Popup):
    def update_result(self, query):
        self.users_disp.clear_widgets()

        add = self.users_disp.add_widget
        for online, name in app.search_username(query):
            add(SearchRecord(self, online, name))

    def on_dismiss(self):
        if not self.keep_text:
            self.tx_nick.text = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Add a user'
        self.size_hint = (None, None)
        self.size = 400, 350
        self.keep_text = False
        self.box = BoxLayout(orientation = 'vertical',
                             spacing = 15,
                             padding = 10)
        self.tx_nick = SearchInput(self,
                                   'Enter a username...',
                                   size_hint = (1, 0.12),
                                   multiline = False,
                                   font_size = 13,
                                   on_text = self.update_result)

        self.disp_scroll = FramedScrollView(bar_inactive_color = (0, 0, 0, 0),
                                            bar_color = (0.3, 0.3, 0.3, 0.7),
                                            bar_margin = 3,
                                            do_scroll_x = False,
                                            size_hint = (1, 0.88))
        self.users_disp = GridLayout(cols = 1,
                                     size_hint_y = None)
        self.users_disp.bind(minimum_height = self.users_disp.setter('height'))

        self.msg_popup = Popup(height = 180,
                               title = 'Message (optional)',
                               title_font = 'fonts/OpenSans-Regular.ttf')
        self.msg_cont = FloatLayout()
        self.msg_input = MessageInput('',
                                      size_hint = (0.98, 0.65),
                                      font_size = 13,
                                      pos_hint = {"top": 0.95, "center_x": 0.5})
        self.msg_confirm = Button(size_hint = (0.4, 0.25),
                                  pos_hint = {"top": 0.22, "right": 0.94},
                                  text = "Confirm",
                                  font_size = 15,
                                  background_normal = "textures/button/normal_intro.png",
                                  background_down = "textures/button/down_intro.png")

        self.msg_cont.add_widget(self.msg_input)
        self.msg_cont.add_widget(self.msg_confirm)
        self.msg_popup.content = self.msg_cont

        self.add_widget(self.box)
        self.box.add_widget(self.tx_nick)
        self.box.add_widget(self.disp_scroll)
        self.disp_scroll.add_widget(self.users_disp)


class MsgInfoPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.info_view = InfoView()

        self.height = 250
        self.content = self.info_view
        self.title = "Message Info"


class DialogScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.msg_stack = []
        self.smiles = [':)', ':D', ':]', ':3', '=)', ':D',
                       'xD', '=D', '>:(', ':-(', ':(', ':c',
                       ':<', ':[', ':{', ':\'(', ':\'-)',':P',
                       ':\')', '>:O', ':o', 'O_O', 'O_o', 'XP',
                       ':*', ';-)', ';)', ';-]', ';]', ';D',
                       ':-p', ':p', ':-Þ', ':Þ', ':þ', ':-b',
                       ':b', '>:/', ':-.', ':/', '=/', '>:P',
                       ':L', '>.<', '-_-', ':|', 'O:-)', '0:3',
                       '0:)', '>:)', '>;)', '>:-)', '%)', '<:-|',
                       '</3', '<3', '^_^', '^^', '(._.)', '/(._. )']

        self.main_box = BoxLayout(orientation = "vertical")

        self.button_bar = DialogButtonBar(self,
                                          size_hint = (1, 0.06))
        self.status_bar = DialogStatusBar(size_hint = (1, 0.06))

        self.msg_layout = MessageView(size_hint = (1, 0.66),
                                      bar_inactive_color = (0, 0, 0, 0),
                                      do_scroll_x = False,
                                      bar_margin = 3,)

        self.msg_grid = GridLayout(cols = 1,
                                   padding = 10,
                                   spacing = 10,
                                   size_hint_y = None)
        self.msg_grid.bind(minimum_height = self.msg_grid.setter('height'))
        # For modifying the height when new widgets are added

        self.input_bar = DialogInputBar(size_hint = (1, 0.2))

        self.smile_bbl = SmileBubble()
        grid = self.smile_bbl.ids['smile_grid']
        for smile in self.smiles:
            grid.add_widget(SmileButton(text=smile,
                                        on_release = self.input_bar.add_smile,
                                        background_normal = '',
                                        background_down = '',
                                        background_color = (0, 0, 0, 0),
                                        font_size = 13,
                                        always_release = True,
                                        font_name = "fonts/OpenSans-Semibold.ttf"))

        self.info_popup = MsgInfoPopup()

        self.add_widget(self.main_box)
        self.main_box.add_widget(self.button_bar)
        self.main_box.add_widget(self.status_bar)
        self.main_box.add_widget(self.msg_layout)
        self.main_box.add_widget(self.input_bar)

        self.msg_layout.add_widget(self.msg_grid)


class DialogButton(Button):
    pass


class DialogOptButton(Button):
    def __init__(self, sym, text, space, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.font_size = 13
        self.background_normal = 'textures/button/drop_opt.png'
        self.background_down = 'textures/button/drop_opt_down.png'
        self.font_name = 'fonts/ionicons_regular.ttf'
        self.height = 25
        self.markup = True
        self.text = '[size=18]' + sym + '[/size] ' + \
                    ' ' * space + text + ' ' * space


class DialogButtonBar(BoxLayout):
    def drop_open(self, bt):
        self.opts_drop.open(self.opts_extender)

    def search_msg(self, bt):
        self.opts_drop.dismiss()
        SearchMsgPopup(self.scr).open()

    def __init__(self, scr, **kwargs):
        super().__init__(**kwargs)
        self.scr = scr
        self.menu = DialogButton(text = ' Menu',
                                 halign = 'left',
                                 size_hint = (0.19, 1),
                                 on_release = app.to_menu)
        self.opts_drop = DropDown()
        self.opts_extender = BoxLayout(size_hint = (0.46, 1))
        self.opts = DialogButton(text = 'Options ',
                                 halign = 'right',
                                 on_release = self.drop_open)
        self.plc = Button(background_disabled_normal =
                          'textures/button/menu_bt_normal.png',
                          disabled = True,
                          size_hint = (0.35, 1))
        self.opts_plc = Button(background_disabled_normal =
                               'textures/button/menu_bt_normal.png',
                               disabled = True)

        self.search_bt = DialogOptButton('', 'Search for messages', 1,
                                         on_release = self.search_msg)
        self.delete_bt = DialogOptButton('', 'Delete dialog', 9,
                                         on_release = app.delete_dialog)
        self.opts_drop.add_widget(self.search_bt)
        self.opts_drop.add_widget(self.delete_bt)

        self.opts_extender.add_widget(self.opts_plc)
        self.opts_extender.add_widget(self.opts)

        self.add_widget(self.menu)
        self.add_widget(self.plc)
        self.add_widget(self.opts_extender)


class SearchMsgButton(Button):
    def on_release(self):
        l_tm = self.cont.from_picker.timestamp
        u_tm = self.cont.to_picker.timestamp
        text = self.cont.text_to_search.text
        if l_tm > u_tm:
            ErrorDisp('The end time exceeds the beginning.').open()
        else:
            msgs = app.search_message(self.cont.scr, text, l_tm, u_tm)
            self.cont.build_msgs(msgs)

    def __init__(self, cont, **kwargs):
        super().__init__(**kwargs)
        self.cont = cont
        self.font_name = 'fonts/ionicons_regular.ttf'
        self.background_normal = 'textures/button/normal.png'
        self.background_down = 'textures/button/down.png'


class SearchMsgPopup(Popup):
    def build_msgs(self, msg_list):
        self.msg_grid.clear_widgets()
        for text, curr_time, nick in msg_list:
            msg_row = MessageRow(text,
                                 curr_time,
                                 escape_markup(nick),
                                 self.scr)

            self.msg_grid.add_widget(msg_row)

    def __init__(self, scr, **kwargs):
        super().__init__(**kwargs)
        self.title = "Search messages"
        self.size = (300, 400)
        self.scr = scr

        self.container = BoxLayout(orientation = "vertical",
                                   padding = 10,
                                   spacing = 10)
        self.from_box = BoxLayout(size_hint = (1, 0.1))
        self.to_box = BoxLayout(size_hint = (1, 0.1))

        self.from_lb = Label(text = "From: ",
                             size_hint = (0.2, 1),
                             color = (1, 1, 1, 1))
        self.to_lb = Label(text = "To: ",
                           size_hint = (0.2, 1),
                           color = (1, 1, 1, 1))
        self.from_picker = ExtendedDatePicker()
        self.to_picker = ExtendedDatePicker()

        self.from_box.add_widget(self.from_lb)
        self.from_box.add_widget(self.from_picker)
        self.to_box.add_widget(self.to_lb)
        self.to_box.add_widget(self.to_picker)

        self.src_button = SearchMsgButton(self,
                                          text = " Search",
                                          size_hint = (1, 0.1))

        self.text_to_search = MessageInput("Text to search...",
                                           size_hint = (1, 0.3),
                                           font_size = 13)

        self.msg_layout = MessageView(size_hint = (1, 0.5),
                                      bar_inactive_color = (0, 0, 0, 0),
                                      do_scroll_x = False,
                                      bar_margin = 3,)

        self.msg_grid = GridLayout(cols = 1,
                                   padding = 10,
                                   spacing = 10,
                                   size_hint_y = None)
        self.msg_grid.bind(minimum_height = self.msg_grid.setter('height'))

        self.msg_layout.add_widget(self.msg_grid)

        self.container.add_widget(self.from_box)
        self.container.add_widget(self.to_box)
        self.container.add_widget(self.text_to_search)
        self.container.add_widget(self.src_button)
        self.container.add_widget(self.msg_layout)

        self.content = self.container


class DialogStatusBar(BoxLayout):
    def view_profile(self, bt):
        app.to_profile(self.name.text)

    def update_names(self, bt):
        self.nick = app.login_scr.tx_usr.text
        if not self.nick:
            self.nick = app.register_scr.tx_usr.text
        self.self_name.text = self.nick

        self.name.text = app.person
        self.status.online = bt.parent.status.online

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.self_name = NickLabel(halign = "right",
                                   on_release = app.to_self_profile)
        self.self_status = Status(size_hint = (0.1, 1))

        self.name = NickLabel(halign = "left",
                              on_release = app.to_profile)
        self.status = Status(size_hint = (0.1, 1))

        self.add_widget(self.self_status)
        self.add_widget(self.self_name)
        self.add_widget(Widget())
        self.add_widget(self.name)
        self.add_widget(self.status)


class MessageRow(BoxLayout):
    def __init__(self, text, tm, sender, scr, **kwargs):
        super().__init__(**kwargs)
        self.scr = scr

        self.msg = Message(text, tm, sender, scr,
                           size_hint = (0.7, 1))
        self.tm = ClockLabel(tm,
                             size_hint = (0.1, 1))

        self.height = self.msg.height
        self.size_hint = [1, None]

        if sender != app.nick:
            self.add_widget(Widget(size_hint = (0.2, 1)))
            self.add_widget(self.tm)
            self.add_widget(self.msg)
        else:
            self.add_widget(self.msg)
            self.add_widget(self.tm)
            self.add_widget(Widget(size_hint = (0.2, 1)))


class DialogInputBar(BoxLayout):
    def smile_show(self, bt):
        if self.scr is None:
            self.scr = self.parent.parent
        if self.scr.smile_bbl.hidden:
            self.scr.add_widget(self.scr.smile_bbl)
            self.scr.smile_bbl.hidden = False
        else:
            self.scr.remove_widget(self.scr.smile_bbl)
            self.scr.smile_bbl.hidden = True

    def send_msg(self, bt):
        text = self.msg_input.text.strip('\n ')
        self.msg_input.text = ''
        if text not in string.whitespace:
            self.msg_in(text, app.nick)
            self.auto_response(text.upper())

    def auto_response(self, text):
        self.msg_in(text, app.person)

    def msg_in(self, text, nick):
        curr_time = int(time.time() * 100)
        if self.scr is None:
            self.scr = self.parent.parent
        msg_row = MessageRow(text, curr_time, escape_markup(nick), self.scr)

        self.scr.msg_grid.add_widget(msg_row)
        self.scr.msg_layout.scroll_to(msg_row)

    def add_smile(self, bt):
        self.msg_input.text += ' ' + bt.text + ' '

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.btn_panel = BoxLayout(orientation = "vertical",
                           size_hint = (0.1, 1))

        self.input_panel = InputBox(size_hint = (0.9, 1))

        self.msg_input = MessageInput('Your message here...',
                                      font_size = 13)

        self.bt_send = InputButton(size_hint = (1, 0.35),
                                   text = "",
                                   font_size = 20,
                                   on_release = self.send_msg)

        self.bt_smile = InputButton(size_hint = (1, 0.65),
                                    text = "",
                                    font_size = 22,
                                    on_release = self.smile_show)

        self.scr = None

        self.add_widget(self.input_panel)
        self.add_widget(self.btn_panel)

        self.input_panel.add_widget(self.msg_input)

        self.btn_panel.add_widget(self.bt_smile)
        self.btn_panel.add_widget(self.bt_send)


class ChatApp(App):
    nick_ptrn = re.compile('(?![ ]+)[\w ]{2,15}')
    invalid_nick = ('The username you entered is incorrect. '
                    'It should only consist of letters and spaces, '
                    'it cannot consist of spaces only and must be '
                    '2 to 15 characters long')
    nick_taken = ('There is already a user with the username you entered. '
                  'Try something different')
    wrong_pswd = ('You entered a wrong password for this username. '
                  'Try again')
    users = [[('user1', True),
              ('user7', False)],
             [('user2', False)],
             [('user3', True)],
             [('user4', False)],
             [('user5', True)],
             [('user6', False)]]

    def to_login(self, bt = None):
        Window.size = (370, 200)
        self.screens.transition = self.no_trans
        self.screens.current = 'login'

    def to_register(self, bt = None):
        Window.size = (370, 240)
        self.screens.transition = self.no_trans
        self.screens.current = 'register'

    def to_self_profile(self, bt = None):
        Window.size = (350, 500)
        self.screens.transition = self.no_trans
        self.screens.current = 'self_profile'

    def to_menu(self, bt = None):
        Window.size = (500, 450)
        self.screens.transition = self.no_trans
        self.screens.current = 'menu'

    def to_profile(self, nick, from_search = False):
        if from_search:
            p = self.menu_scr.add_person_popup
            p.keep_text = True
            p.dismiss()
            p.keep_text = False

        Window.size = (350, 500)
        self.screens.current = 'profile'

    def to_settings(self, bt = None):
        pass

    def to_help(self, bt = None):
        pass

    def to_dialog(self, bt):
        Window.size = (350, 500)
        name = bt.text
        self.person = name
        self.screens.get_screen(name).status_bar.update_names(bt)

        self.screens.current = self.person

    def add_favs(self, bt = None):
        print('add_favs')

    def remove_favs(self, bt = None):
        print('remove_favs')

    def add_friends(self, bt = None):
        print('add_friends')

    def remove_friends(self, bt = None):
        print('remove_friends')

    def add_bl(self, bt = None):
        print('add_bl')

    def remove_bl(self, bt = None):
        print('remove_bl')

    def get_request_msg(self, bt = None):
        print('get_request_msg')

    def accept_request(self, bt = None):
        print('accept_request')

    def decline_request(self, bt = None):
        print('decline_request')

    def take_request_back(self, bt = None):
        print('take_request_back')

    def send_request(self, bt = None):
        print('send_request')

    def get_user_groups(self, bt = None):
        self.menu_scr.build_usr_list(self.users)
        for i in (name[0] for group in self.users for name in group):
            self.screens.add_widget(DialogScreen(name = i))

    def delete_dialog(self, bt = None):
        pass

    def register(self, bt = None):
        if not re.match(self.nick_ptrn,
                        self.register_scr.tx_usr.text):
            ErrorDisp(self.invalid_nick).open()
        elif not 'username_free':
            ErrorDisp(self.nick_taken).open()
        else:
            'register'
            av = _Image.open('textures/panels/avatar_placeholder.png')
            av.save('temp/self_avatar.png', 'PNG')
            av.close()

            self.menu_scr.info_box.avatar.source = 'temp/self_avatar.png'

            self.nick = self.register_scr.tx_usr.text
            self.menu_scr.info_box.logged_as_lb.text = "Logged in as\n" + self.nick

            self.get_user_groups()

            self.to_menu()

    def login(self, bt = None):
        if not 'password_correct':
            ErrorDisp(self.wrong_pswd).open()
        else:
            'login'
            av = _Image.open('textures/panels/avatar_placeholder.png')
            av.save('temp/self_avatar.png', 'PNG')
            av.close()

            self.menu_scr.info_box.avatar.source = 'temp/self_avatar.png'

            self.nick = self.login_scr.tx_usr.text
            self.menu_scr.info_box.logged_as_lb.text = "Logged in as\n" + self.nick

            self.get_user_groups()

            self.to_menu()

    def logout(self, bt = None):
        self.login_scr.tx_usr.text = ''
        self.login_scr.tx_pass.text = ''
        self.register_scr.tx_usr.text = ''
        self.register_scr.tx_pass.text = ''
        self.to_login()

    def search_username(self, query):
        'search_username'
        return [(query, True),
                (query + '1', False)]

    def search_message(self, screen, text, l_tm, u_tm):
        return ((text + 'lol', (u_tm - l_tm) // 2, screen.name),
                (text + 'kek', (u_tm - l_tm) // 2, self.nick))

    def _line_wrap(self, text):
        max_line_len = 22
        if len(text) < max_line_len:
            return text
        dist_right = text[max_line_len:].find(' ')
        ind_left = text[:max_line_len].rfind(' ')
        dist_left = max_line_len - ind_left
        ind_right = dist_right + max_line_len
        if dist_right is -1:
            if ind_left is -1:
                return text[:max_line_len].strip() + '\n' + self._line_wrap(text[max_line_len:].strip())
            return text[:ind_left].strip() + '\n' + self._line_wrap(text[ind_left+1:].strip())
        if ind_left is -1 or dist_left > dist_right:
            lb = Label(text = text[:ind_right])
            lb._label.refresh()
            if lb._label.texture.size[0] < 308:
                return text[:ind_right].strip() + '\n' + self._line_wrap(text[ind_right+1:].strip())
            return text[:max_line_len].strip() + '\n' + self._line_wrap(text[max_line_len:].strip())
        return text[:ind_left].strip() + '\n' + self._line_wrap(text[ind_left+1:].strip())

    def line_wrap(self, text):
        lb = Label(text = text)
        lb._label.refresh()
        text_width = lb._label.texture.size[0]
        if text_width > 230:
            return self._line_wrap(text).rstrip()
        return text

    def send_msg(self, bt):
        text = self.msg_input.text.strip('\n ')
        self.msg_input.text = ''
        if text not in string.whitespace:
            self.msg_in(text, self.nick)
            self.auto_response(text.upper())

    def auto_response(self, text):
        self.msg_in(text, self.person)

    def msg_in(self, text, nick):
        msg_stack = self.msg_stack
        curr_time = datetime.now()
        msg = Message(escape_markup(nick), curr_time)
        msg_stack.append(msg)

        msg.ids['msg'].real_text = text
        msg.ids['msg'].text = self.line_wrap(text)

        msg.size_hint = [None, None]
        msg.width = self.width_modify(msg)
        msg.height = (len(msg.ids['msg']._lines_labels) + 1) * msg.ids['msg'].line_height

        if nick != self.nick:
            msg_stack[-1].bg_color = [0.91, 0.95, 1, 1]

        for i in msg.walk():
            i.height = msg.height
            i.width = msg.width
            i.x = msg.x

        self.msg_grid.add_widget(msg)
        self.msg_layout.scroll_to(msg)

    def log_in(self, bt):
        self.nick = self.tx_usr.text
        self.my_name.text = self.nick
        self.my_profile.ids['nick'].text = self.nick
        self.passw = self.tx_pass.text
        self.person = self.drop_mnt.ids['name'].text
        self.person_name.text = self.person
        self.person_profile.ids['nick'].text = self.person
        if self.nick or self.passw:
            self.screens.current = 'main'
            Window.size = (350, 500)

    def show_help(self, bt):
        self.slide_trans.direction = "down"
        self.screens.transition = self.slide_trans
        self.screens.current = 'help'

    def on_stop(self):
        for i in os.scandir('temp'):
            os.remove(i.path)
        os.rmdir('temp')

    def build(self):
        Window.clearcolor = (0.71, 0.85, 1, 1)
        self.nick = ''
        self.person = ''
        self.msg_stack = []

        self.people = ["UpperBot"]

        self.no_trans = NoTransition()

        self.slide_trans = SlideTransition(direction = "up")

        self.screens = ScreenManager(transition = self.no_trans)

        self.register_scr = RegScreen(name = "register")
        self.login_scr = LoginScreen(name = "login")
        self.menu_scr = MenuScreen(name = "menu")
        #self.dialog_scr = DialogScreen(name = "dialog")
        self.help = Screen(name = "help")
        self.self_profile_scr = SelfProfile(name = "self_profile")
        self.profile_scr = PersonProfile(name = "profile")

        self.help_box = BoxLayout(orientation = "vertical")

        self.help_bar = HelpBar(size_hint = (1, 0.064))

        self.help_text = HelpLabel()

        self.screens.add_widget(self.register_scr)
        self.screens.add_widget(self.login_scr)
        self.screens.add_widget(self.menu_scr)
        #self.screens.add_widget(self.dialog_scr)
        self.screens.add_widget(self.help)
        self.screens.add_widget(self.self_profile_scr)
        self.screens.add_widget(self.profile_scr)

        self.help.add_widget(self.help_box)

        self.help_box.add_widget(self.help_bar)
        self.help_box.add_widget(self.help_text)
        return self.screens


if __name__ == "__main__":
    app = ChatApp()
    app.run()