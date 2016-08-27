from kivy import require
require('1.9.1')

from kivy.config import Config
Config.set('graphics', 'width', 370)
Config.set('graphics', 'height', 240)
Config.set('graphics', 'resizable', False)

import string, re
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.effects.scroll import ScrollEffect
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, SlideTransition
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
from kivy.uix.spinner import Spinner
from kivy.clock import Clock

Builder.load_string('''
<Label>:
    font_name: "fonts/OpenSans-Regular.ttf"
    halign: "center"
    color: 0, 0, 0, 1

<Button>:
    color: 1, 1, 1, 1

<Popup>:
    size_hint: None, None
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    width: 250
    separator_height: 1
    title_font: "fonts/ionicons_semibold.ttf"

<ChatTopBar>:
    ChatTopButton:
        text: " Settings"
        size_hint: 0.5, 1
    ChatTopButton:
        text: " Help"
        size_hint: 0.4, 1
        on_release: app.show_help(self)
    ChatTopButton:
        disabled: True
    ChatTopButton:
        text: " Log out"
        size_hint: 0.5, 1
        on_release: app.logout_dialog.open()

<ChatTopButton@Button>:
    background_normal: 'textures/button/menu_bt_normal.png'
    background_down: 'textures/button/inputbt_down.png'
    background_disabled_normal: 'textures/button/menu_bt_normal.png'
    font_size: 13
    font_name: 'fonts/ionicons_semibold.ttf'

<DateSpinner>:
    sync_height: True
    text_autoupdate: True
    background_normal: 'textures/button/normal.png'
    background_down: 'textures/button/down.png'
    background_disabled_normal: 'textures/button/disabled.png'
    disabled_color: 1, 1, 1, 1

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
            points: self.x, self.y + self.height,\
            self.x + self.width, self.y + self.height,\
            self.x + self.width, self.y, self.x, self.y,\
            self.x, self.y + self.height
    markup: True
    font_name: 'fonts/OpenSans-Regular.ttf'
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

<InfoView>:
    orientation: "vertical"
    Label:
        id: sent_text
        markup: True
        halign: "left"
        text: root.sent_text
        text_size: self.size
        size_hint: 1, 0.4
        font_size: 15
        color: 1, 1, 1, 1

    Label:
        id: msg
        text: "Message text:"
        font_name: "fonts/OpenSans-Semibold.ttf"
        size_hint: 1, 0.15
        font_size: 13
        color: 1, 1, 1, 1

    TextInput:
        id: msg_text
        readonly: True
        cursor_color: 0, 0, 0, 0
        background_normal: "textures/textinput/msginput_unfocused.png"
        background_active: "textures/textinput/msginput_unfocused.png"

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

<LogoutButton>:
    background_normal: 'textures/button/normal.png'
    background_down: 'textures/button/down.png'
    background_disabled_normal: 'textures/button/disabled.png'
    font_name: 'fonts/ionicons_semibold.ttf'

#<MenuButton>:
    #font_size: 16
    #font_name: 'fonts/ionicons_semibold.ttf'
    #size_hint: 1, 0.1

<Message>:
    width: 500
    BoxLayout:
        pos: root.pos
        height: self.height
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

        TextInput:
            id: msg
            pos: root.pos
            size: root.size
            font_name: "fonts/OpenSans-Regular.ttf"
            font_size: 13
            background_color: 0, 0, 0, 0
            readonly: True
            cursor_color: 0, 0, 0, 0

<MessageInput>:
    background_normal: 'textures/textinput/msginput_unfocused.png'
    background_active: 'textures/textinput/msginput_focused.png'
    font_size: 13
    font_name: "fonts/OpenSans-Regular.ttf"
    cursor_color: 0, 0, 0, 1
    write_tab: False
    hint_text: self.placeholder

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
            points: self.x, self.y + self.height,\
            self.x + self.width, self.y + self.height,\
            self.x + self.width, self.y, self.x, self.y,\
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
    color: [1, 1, 1, 1] if self.state is 'normal' else [0.16, 0.36, 0.56, 1]
    size_hint_x: None
    width: self.texture_size[0]
    font_size: 13

<PersonLayout>:
    canvas.after:
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Line:
            points: self.x, self.y + self.height,\
            self.x + self.width, self.y + self.height,\
            self.x + self.width, self.y, self.x, self.y,\
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
        on_release: app.hide_screen(self, 'right')
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
    font_name: 'fonts/ionicons_regular.ttf'
    markup: True

<RegLabel>:
    color: 1, 1, 1, 1
    font_name: 'fonts/ionicons_semibold.ttf'
    size_hint: 0.7, 1
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

<Status>:
    size_hint_x: None
    width: 30
    canvas:
        Color:
            rgba: 0, 0, 0, 1
        Ellipse:
            pos: self.x + 9, self.y + 9
            size: 12, 12
        Color:
            rgba: [0.5, 0.9, 0, 1] if root.online else [0.67, 0.79, 0.91, 1]
        Ellipse:
            pos: self.x + 10, self.y + 10
            size: 10, 10

<ErrorLabel>:
    text_size: self.size
    halign: "left"
    valign: "top"
''')

class SmileButton(Button):
    def on_press(self):
        self.color = (0.6, 0.8, 1, 1)

    def on_release(self):
        self.color = (1, 1, 1, 1)

class Message(Widget):
    bg_color = ListProperty([0.99, 0.99, 0.99, 1])
    real_text = StringProperty()
    def __init__(self, sender, time, **kwargs):
        self.sender = sender
        self.time = time
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            sent = "Sender: [color=#B6DAFF]{}[/color]\nTime: [color=#C8C8C8]{}[/color]".format(self.sender, self.time.strftime("%H:%M:%S"))
            info_view = app.info_view
            info_popup = app.info_popup
            info_view.ids['sent_text'].text = sent
            info_view.ids['msg_text'].text = self.ids['msg'].real_text
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

class Status(Widget):
    online = BooleanProperty(True)

class NickLabel(Button):
    pass

class InfoView(BoxLayout):
    def __init__(self, **kwargs):
        self.sent_text = ''
        super().__init__(**kwargs)

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

class LogoutButton(Button):
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

class MyProfile(Profile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids['avatar'].ids['src'].source = 'rogue.jpg'

class MessageInput(TextInput):
    def __init__(self, **kwargs):
        self.placeholder = 'Your message here...'
        super().__init__(**kwargs)

    def on_focus(self, inst, focus):
        self.hint_text = '' if focus or self.text else self.placeholder

class InputBox(BoxLayout):
    pass

class InputButton(Button):
    pass

class DateSpinner(Spinner):
    pass

class DatePicker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        curr_year = datetime.now().year
        self.day = DateSpinner(size_hint = (0.2, 1),
                           values = map(str, range(1, 32)))

        self.month = DateSpinner(size_hint = (0.5, 1),
                             values = ('January', 'February', 'March', 'April',
                                       'June', 'July', 'August', 'September',
                                       'October', 'November', 'December'))

        self.year = DateSpinner(size_hint = (0.3, 1),
                            values = map(str, range(1970, curr_year + 1)))

        self.add_widget(self.day)
        self.add_widget(self.month)
        self.add_widget(self.year)

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

        self.to_login = InputButton(size_hint = (0.3, 1),
                                    font_name = "fonts/ionicons_semibold.ttf",
                                    text = " Login",
                                    on_release = app.to_login,
                                    background_normal = 'textures/button/topbt_normal.png')

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
                                     font_name = 'fonts/ionicons_regular.ttf',
                                     text = ' Show password',
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
        cont = FloatLayout()
        btn = Button(size_hint = (0.4, 0.2),
                     pos_hint = {"top": 0.163, "right": 0.94},
                     text = "Back",
                     font_size = 15,
                     background_normal = "textures/button/normal_intro.png",
                     background_down = "textures/button/down_intro.png",
                     on_release = self.dismiss)
        lb = ErrorLabel(text = text,
                        font_size = 13,
                        color = (1, 1, 1, 1),
                        size_hint = (0.95, 0.8),
                        pos_hint = {"top": 0.99, "center_x": 0.5},
                        halign = "left",
                        valign = "top")

        cont.add_widget(lb)
        cont.add_widget(btn)
        super().__init__(title = 'Error',
                         content = cont,
                         height = 180,
                         **kwargs)

class MenuButton(Button):
    pass

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.left_bar = BoxLayout(size_hint = (0.4, 1))
        self.right_bar = BoxLayout(size_hint = (0.6, 1))

        self.menu_label = RegLabel(text = "Menu")
        self.info_box = FloatLayout()
        self.profile_bt = MenuButton()
        self.logout_bt = MenuButton()
        self.settings_bt = MenuButton()
        self.help_bt = MenuButton()
        self.quit_bt = MenuButton()

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

        self.to_register = InputButton(size_hint = (0.3, 1),
                                       font_name = "fonts/ionicons_semibold.ttf",
                                       text = "[size=18][/size] Register",
                                       markup = True,
                                       on_release = app.to_register,
                                       background_normal = 'textures/button/topbt_normal.png')

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
                              pos_hint = {"top": 0.16, "right": 0.94},
                              text = "Next",
                              font_size = 16,
                              disabled = True,
                              background_normal = "textures/button/normal_intro.png",
                              background_down = "textures/button/down_intro.png",
                              background_disabled_normal = "textures/button/disabled_intro.png",
                              on_release = app.login)

        self.show_psw = ShowPswdButton(size_hint = (0.4, 0.15),
                                     pos_hint = {"top": 0.16, "right": 0.4},
                                     font_name = 'fonts/ionicons_regular.ttf',
                                     text = ' Show password',
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

    def to_login(self, bt):
        Window.size = (370, 200)
        self.screens.transition = self.no_trans
        self.screens.current = 'login'

    def to_register(self, bt):
        Window.size = (370, 240)
        self.screens.transition = self.no_trans
        self.screens.current = 'register'

    def to_menu(self, *args):
        Window.size = (500, 450)
        self.screens.current = 'menu'

    def register(self, bt):
        if not re.match(self.nick_ptrn,
                        self.register_scr.tx_usr.text):
            ErrorDisp(self.invalid_nick).open()
        elif not 'username_free':
            ErrorDisp(self.nick_taken).open()
        else:
            'register'
            self.to_menu()

    def login(self, bt):
        if not 'password_correct':
            ErrorDisp(self.wrong_pswd).open()
        else:
            'login'
            self.to_menu()

    def width_modify(self, inst):
        min_width = 160
        max_width = 320
        max_line = 0
        for i in inst.ids['msg']._lines_labels:
            if i.width > max_line:
                max_line = i.width
        curr_width = max_line + 15
        if curr_width < min_width:
            return min_width
        elif curr_width > max_width:
            return max_width
        else:
            return curr_width

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

    def drop_open(self, bt):
        self.drop_picker.open(self.drop_mnt)

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

    def smile_show(self, bt):
        if self.smile_bbl.hidden:
            self.chat.add_widget(self.smile_bbl)
            self.smile_bbl.hidden = False
        else:
            self.chat.remove_widget(self.smile_bbl)
            self.smile_bbl.hidden = True

    def smile_in(self, bt):
        self.msg_input.text += ' ' + bt.text + ' '

    def log_out_next(self, bt):
        self.screens.transition = self.no_trans
        self.screens.current = 'intro'
        Window.size = (400, 175)
        self.nick = ''
        self.passw = ''

    def log_out_anim(self, bt):
        self.logout_dialog.dismiss()
        Clock.schedule_once(self.log_out_next, 0.1)

    def show_help(self, bt):
        self.slide_trans.direction = "down"
        self.screens.transition = self.slide_trans
        self.screens.current = 'help'

    def hide_screen(self, bt, direct):
        self.screens.transition.direction = direct
        self.screens.current = 'main'

    def show_profile(self, bt):
        self.slide_trans.direction = "left"
        self.screens.transition = self.slide_trans
        who = 'my' if bt is self.my_name else 'person'
        self.screens.current = who + '_profile'

    def hide_profile(self, bt):
        self.screens.transition.direction = "right"
        self.screens.current = 'main'

    def build(self):
        Window.clearcolor = (0.71, 0.85, 1, 1)
        self.nick = ''
        self.person = ''
        self.msg_stack = []
        self.smiles = [':)', ':D', ':]', ':3', '=)',
                       ':D', 'xD', '=D', '>:(', ':-(', ':(',
                       ':c', ':<', ':[', ':{', ':\'(',
                       ':\'-)', ':\')', '>:O', ':o',
                       'O_O', 'O_o', ':*', ';-)', ';)',
                       ';-]', ';]', ';D', '>:P', ':P', 'XP',
                       ':-p', ':p', ':-Þ', ':Þ', ':þ', ':-b',
                       ':b', '>:/', ':-.', ':/', '=/',
                       ':L', '>.<', '-_-', ':|', 'O:-)', '0:3',
                       '0:)', '>:)', '>;)', '>:-)', '%)', '<:-|',
                       '</3', '<3', '^_^', '^^', '(._.)', '/(._. )']

        self.people = ["UpperBot"]

        self.no_trans = NoTransition()

        self.slide_trans = SlideTransition(direction = "up")

        self.screens = ScreenManager(transition = self.no_trans)

        #self.intro = Screen(name = "intro")
        self.register_scr = RegScreen(name = "register")
        self.login_scr = LoginScreen(name = "login")
        self.menu_scr = MenuScreen(name = "menu")
        self.chat = Screen(name = "main")
        self.help = Screen(name = "help")
        self.my_profile = MyProfile(name = "my_profile")
        self.person_profile = PersonProfile(name = "person_profile")

        #self.intro_box = BoxLayout()
        #self.reg_box = RegisterLayout(size_hint = (0.7, 1))
        #self.name_box = PersonLayout(size_hint = (0.3, 1))

        #self.lb_reg = RegLabel(size_hint = (1, 0.17),
                               #pos_hint = {"top": 1},
                               #text = "Register")

        #self.lb_usr = Label(size_hint = (0.28, 0.1),
                            #pos_hint = {"top": 0.7, "right": 0.3},
                            #text = "Username:",
                            #color = (1, 1, 1, 1),
                            #font_size = 16)

        #self.tx_usr = NickInput(size_hint = (0.6, 0.19),
                                #pos_hint = {"top": 0.755, "right": 0.95})

        #self.lb_pass = Label(size_hint = (0.28, 0.1),
                             #pos_hint = {"top": 0.45, "right": 0.3},
                             #text = "Password:",
                             #color = (1, 1, 1, 1),
                             #font_size = 16)

        #self.tx_pass = NickInput(size_hint = (0.6, 0.19),
                                 #pos_hint = {"top": 0.495, "right": 0.95},
                                 #password = True)

        #self.bt_next = Button(size_hint = (0.5, 0.2),
                              #pos_hint = {"top":0.19, "right":0.94},
                              #text = "Next",
                              #font_size = 16,
                              #disabled = True,
                              #background_normal = "textures/button/normal_intro.png",
                              #background_down = "textures/button/down_intro.png",
                              #background_disabled_normal = "textures/button/disabled_intro.png",
                              #on_release = self.log_in)

        #self.lb_who = RegLabel(size_hint = (1, 0.25),
                               #pos_hint = {"top": 1, "right": 1},
                               #font_size = 13,
                               #text = "Who do you want\nto chat with?")

        #self.drop_picker = ChatPicker(max_height = 1)

        #for i in self.people:
            #bt = Button(size_hint = (0.9, None),
                         #height = 24,
                         #text = i,
                         #font_size = 11,
                         #color = (0, 0, 0, 1),
                         #background_normal = "textures/button/drop_opt.png",
                         #background_down = "textures/button/drop_opt_down.png",
                         #on_release = lambda bt: self.drop_picker.select(bt.text))
            #self.drop_picker.add_widget(bt)

        #self.drop_mnt = PickerHead(size_hint = (0.9, None),
                                   #height = 24,
                                   #pos_hint = {"top": 0.7, "right": 0.95})

        #self.drop_mnt.ids['arrow'].bind(on_release = self.drop_open)

        self.main_box = BoxLayout(orientation = "vertical")

        self.top_bar = BoxLayout(size_hint = (1, 0.12),
                                 orientation = "vertical")

        self.menu_panel = ChatTopBar(size_hint = (1, None),
                                     height = 30)

        self.status_panel = BoxLayout()

        self.my_name = NickLabel(halign = "right",
                                 on_press = self.show_profile)

        self.person_name = NickLabel(halign = "left",
                                     on_press = self.show_profile)

        self.status_place = Widget()

        self.my_status = Status()

        self.person_status = Status()

        self.msg_layout = MessageView(size_hint = (1, 0.68),
                                      bar_inactive_color = (0, 0, 0, 0),
                                      do_scroll_x = False,
                                      bar_margin = 3)

        self.msg_grid = GridLayout(cols = 1,
                                   padding = 10,
                                   spacing = 10,
                                   size_hint_y = None)
        self.msg_grid.bind(minimum_height = self.msg_grid.setter('height'))
        # For modifying the height when new widgets are added

        self.input_bar = BoxLayout(size_hint = (1, 0.2))

        self.btn_panel = BoxLayout(orientation = "vertical",
                                   size_hint = (0.1, 1))

        self.input_panel = InputBox(size_hint = (0.9, 1))

        self.msg_input = MessageInput()

        self.bt_send = InputButton(size_hint = (1, 0.35),
                                   text = "",
                                   font_size = 20,
                                   on_release = self.send_msg)

        self.bt_smile = InputButton(size_hint = (1, 0.65),
                                    text = "",
                                    font_size = 22,
                                    on_release = self.smile_show)

        self.smile_bbl = SmileBubble()
        grid = self.smile_bbl.ids['smile_grid']
        for smile in self.smiles:
            grid.add_widget(SmileButton(text=smile,
                                        on_release = self.smile_in,
                                        background_normal = '',
                                        background_down = '',
                                        background_color = (0, 0, 0, 0),
                                        font_size = 13,
                                        font_name = "fonts/OpenSans-Semibold.ttf"))

        self.info_view = InfoView()

        self.info_popup = Popup(height = 250,
                                content = self.info_view,
                                title = "Message Info")

        self.help_box = BoxLayout(orientation = "vertical")

        self.help_bar = HelpBar(size_hint = (1, 0.064))

        self.help_text = HelpLabel()

        self.logout_view = BoxLayout(orientation = "vertical")

        self.logout_dialog = Popup(height = 150,
                                   title = " Log out",
                                   title_size = 16,
                                   content = self.logout_view)

        self.logout_ask = Label(size_hint = (1, 0.6),
                                text = "Do you want to log out?",
                                color = (1, 1, 1, 1),
                                font_name = "fonts/ionicons_semibold.ttf")

        self.logout_btns = BoxLayout(size_hint = (1, 0.4),
                                     spacing = 4,
                                     padding = 2)

        self.logout_yes = LogoutButton(text = " Yes",
                                       on_release = self.log_out_anim)

        self.logout_no = LogoutButton(text = " No",
                                      on_release = self.logout_dialog.dismiss)

        self.screens.add_widget(self.register_scr)
        self.screens.add_widget(self.login_scr)
        self.screens.add_widget(self.menu_scr)
        self.screens.add_widget(self.chat)
        self.screens.add_widget(self.help)
        self.screens.add_widget(self.my_profile)
        self.screens.add_widget(self.person_profile)

        #self.intro.add_widget(self.intro_box)
        #self.intro_box.add_widget(self.reg_box)
        #self.intro_box.add_widget(self.name_box)

        #self.reg_box.add_widget(self.lb_reg)
        #self.reg_box.add_widget(self.lb_usr)
        #self.reg_box.add_widget(self.tx_usr)
        #self.reg_box.add_widget(self.lb_pass)
        #self.reg_box.add_widget(self.tx_pass)
        #self.reg_box.add_widget(self.bt_next)

        #self.name_box.add_widget(self.lb_who)
        #self.name_box.add_widget(self.drop_mnt)

        self.chat.add_widget(self.main_box)
        self.main_box.add_widget(self.top_bar)
        self.main_box.add_widget(self.msg_layout)
        self.main_box.add_widget(self.input_bar)

        self.top_bar.add_widget(self.menu_panel)
        self.top_bar.add_widget(self.status_panel)
        self.msg_layout.add_widget(self.msg_grid)

        self.status_panel.add_widget(self.person_status)
        self.status_panel.add_widget(self.person_name)
        self.status_panel.add_widget(self.status_place)
        self.status_panel.add_widget(self.my_name)
        self.status_panel.add_widget(self.my_status)

        self.input_bar.add_widget(self.input_panel)
        self.input_bar.add_widget(self.btn_panel)

        self.input_panel.add_widget(self.msg_input)

        self.btn_panel.add_widget(self.bt_smile)
        self.btn_panel.add_widget(self.bt_send)

        self.help.add_widget(self.help_box)

        self.help_box.add_widget(self.help_bar)
        self.help_box.add_widget(self.help_text)

        self.logout_view.add_widget(self.logout_ask)
        self.logout_view.add_widget(self.logout_btns)

        self.logout_btns.add_widget(self.logout_yes)
        self.logout_btns.add_widget(self.logout_no)

        return self.screens

if __name__ == "__main__":
    app = ChatApp()
    app.run()