# -*- coding: utf-8 -*-
from __future__ import print_function
from time import *
from kivy.app import App
from kivy.config import ConfigParser
from kivy.utils import platform
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.textfields import MDTextField
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty
from kivymd.button import MDRaisedButton, MDIconButton, MDFlatButton, MDFloatingActionButton
from kivymd.label import MDLabel
from kivy.uix.image import Image
from kivymd.toolbar import Toolbar
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.dialog import MDDialog
from kivy.uix.image import Image, AsyncImage
from kivy.uix.scrollview import ScrollView
from kivymd.theming import ThemeManager
from kivy.uix.behaviors import CoverBehavior, ButtonBehavior
from kivymd.list import OneLineRightIconListItem, IRightBodyTouch, TwoLineListItem
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerIconButton, NavigationDrawerDivider
from kivymd.navigationdrawer import NavigationLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivymd.list import OneLineListItem
from kivymd.spinner import MDSpinner
from kivy.clock import Clock
from kivymd.snackbar import Snackbar
from kivy.network.urlrequest import UrlRequest
from kivy.animation import Animation
from kivy.core.clipboard import Clipboard
from kivy.core.image import Image as CoreImage
from kivymd.progressbar import MDProgressBar
from qrcode_gen import QRCodeWidget
from kivy.metrics import dp
from urllib import urlencode, unquote
from kivy.config import Config
from kivy.core.audio import SoundLoader
from threading import Thread
from jsondb import JsonDataBase
from collections import namedtuple
from kivy.utils import platform as PLATFORM
from kivy.logger import Logger
from crypter import *
from hashlib import md5, sha1
from base64 import b64encode, b64decode
from json import dumps, loads
from random import randint
from kivymd.menu import MDDropdownMenu
import os
import zbar
import re
import Image as PIL


# CONSTANTS
Window.softinput_mode = "below_target"
Config.set('kivy', 'exit_on_escape', 0)
DOMAIN = 'https://messengercryptochat.000webhostapp.com/api/'
OLD_DOMAIN = 'http://hometask.pe.hu/messenger/new_scripts/'
HEADER = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}


# GLOBAL OBJECTS
DB = None


kv = '''
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import Clock kivy.clock.Clock
#:import XCamera kivy.garden.xcamera.XCamera


<ZBarCamDesktop@Image>:
    sm:app.sm

<MessageDialogContent@BoxLayout>:
    orientation: 'vertical'
    size_hint_: None
    height: self.minimum_height
    MDLabel:
        text:'Copy text'
        size_hint_: None
        height: self.texture_size[1]
    MDLabel:
        text:'Delete message'
        size_hint_: None
        height: self.texture_size[1]


<ZBarCam>:
    sm:app.sm
    Widget:
        id: proxy
        XCamera:
            id: xcamera
            play: True
            resolution: root.resolution
            allow_stretch: True
            keep_ratio: True
            center: self.size and proxy.center
            size:
                (proxy.height, proxy.width) if root.is_android() \
                else (proxy.width, proxy.height)
            canvas.before:
                PushMatrix
                Rotate:
                    angle: -90 if root.is_android() else 0
                    origin: self.center
            canvas.after:
                PopMatrix


<BottomChatField@BoxLayout>:
    canvas.before:
        Color:
            rgba:(235/255.0,235/255.0,235/255.0,1) if app.theme_cls.theme_style=='Light' else (35/255.0,35/255.0,35/255.0,1)
        Rectangle:
            size:self.size
            pos:self.pos
    orientation:'horizontal'
    size_hint:1,None
    height:self.minimum_height
    padding:5
    MDTextField:
        id:message
        multiline: True
        size_hint: 1,None
        height: self.height if self.height <= Window.height*1.5/10 else Window.height*1.5/10
        hint_text: 'Type a message'
        on_text:
            if self.text == '': self.hint_text = 'Enter message'
            else: self.hint_text = ''
    MDIconButton:
        id: send
        icon: 'send'
        text_color: app.theme_cls.primary_color
        theme_text_color: 'Custom'
        disabled: not bool(message.text and message.text.lstrip())
        on_release: app.sm.get_screen('chat').sndmsg(msg=message.text, tpe='text')









<ContactListItem@OneLineListItem>:
    sm:app.sm
    on_release:Clock.schedule_once(root.preload)

<MText>:
    size_hint:1,None
    height:self.texture_size[1]
    font_style:'Caption'
    theme_text_color: 'Primary'

<FromMSG@BoxLayout>:
    size_hint:1,None
    height:self.minimum_height
    BoxLayout:
        spacing:10
        size_hint:1,None
        height:self.minimum_height
        orientation:'vertical'
        BoxLayout:
            size_hint:1,None
            height:self.minimum_height
            AnchorLayout:
                anchor_x:'right'
                size_hint:txt.width,None
                height:txt.height
                MDLabel:
                    padding:7,7
                    markup:True
                    strip:True
                    canvas.before:
                        Color:
                            rgba: app.theme_cls.primary_color
                        RoundedRectangle:
                            size: self.size
                            id:rct
                            pos: self.pos
                            radius: [13,13,0,13]
                    id:txt
                    text:root.txt
                    text_color: (1,1,1,1)
                    theme_text_color: 'Custom'
                    size_hint:None,None
                    size_hint_max_x:1
                    size:self.texture_size
                    text_size: None,self.height
                    on_size:
                        if self.size[0] > Window.width*3/4: self.text_size[0]=Window.width*3/4
        AnchorLayout:
            anchor_x:'right'
            size_hint:1,None
            height:datetime.height
            MDLabel
                id:datetime
                size_hint:1,None
                height:self.texture_size[1]
                font_style: 'Caption'
                font_size:'12sp'
                theme_text_color: 'Hint'
                text: root.datetime
                halign: 'right'

        AnchorLayout:
            anchor_x:'right'
            size_hint:1,None
            height:stat.height
            MDLabel:
                id:stat
                size_hint:1,None
                height:self.texture_size[1]
                font_style: 'Icon'
                font_size:'17sp'
                theme_text_color: 'Hint'
                text: root.stat
                halign: 'right'



<ToMSG@BoxLayout>:
    size_hint:1,None
    height:self.minimum_height
    BoxLayout:
        spacing:10
        size_hint:1,None
        height:self.minimum_height
        orientation:'vertical'
        BoxLayout:
            size_hint:1,None
            height:self.minimum_height
            AnchorLayout:
                anchor_x:'left'
                size_hint:1,None
                height:txt.height
                MDLabel:
                    padding:7,7
                    strip:True
                    markup:True
                    canvas.before:
                        Color:
                            rgba: (97/255.0,97/255.0,97/255.0,1)
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
                            radius: [13,13,13,0]
                    id:txt
                    text:root.txt
                    strip:True
                    markup:True
                    text_color: (1,1,1,1)
                    theme_text_color: 'Custom'
                    size_hint:None,None
                    size_hint_max_x:1
                    size:self.texture_size
                    text_size: None,self.height
                    on_size:
                        if self.size[0] > Window.width*3/4: self.text_size[0]=Window.width*3/4
        AnchorLayout:
            anchor_x:'left'
            size_hint:1,None
            height:datetime.height
            MDLabel:
                id:datetime
                size_hint:1,None
                height:self.texture_size[1]
                font_style: 'Caption'
                theme_text_color: 'Hint'
                text: root.datetime
                halign: 'left'




<SettingsScreen>:
    sm:app.sm
    BoxLayout:
        orientation:'vertical'
        Toolbar:
            title: 'Settings'
            elevation: 8
            background_palette: 'Primary'
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [['arrow-left', root.exit]]
            background_hue: '500'
        BoxLayout:
            orientation:'vertical'
            ScrollView:
                do_scroll_x:False
                id:scroll


<NewContactScreen@Screen>:
    sm: app.sm
    BoxLayout:
        orientation:'vertical'
        Toolbar:
            title: 'Share contacts'
            elevation: 8
            background_palette: 'Primary'
            left_action_items: [['arrow-left', root.go_back]]
            md_bg_color: app.theme_cls.primary_color
            background_hue: '500'
        BoxLayout:
            orientation:'vertical'
            padding:27
            id:box
            spacing:12



<ChatScreen@Screen>:
    sm: app.sm
    BoxLayout:
        orientation:'vertical'
        Toolbar:
            title: root.chatname
            elevation: 8
            background_palette: 'Primary'
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [['arrow-left', root.exit]]
            background_hue: '500'
        BoxLayout:
            id:frame
            orientation:'vertical'
            ScrollView:
                do_scroll_x:False
                id:scroll
                scroll_type:['bars','content']
                canvas.before:
                    Color:
                        rgba:(240/255.0,240/255.0,240/255.0,1) if app.theme_cls.theme_style=='Light' else (48/255.0,48/255.0,48/255.0,1)
                    Rectangle:
                        size:self.size
                        pos:self.pos
                BoxLayout:
                    id:msg
                    orientation:'vertical'
                    size_hint:(1,None)
                    height:self.minimum_height
                    spacing:20
                    padding:30
            MDFlatButton:
                id:create_chat
                pos_hint:{'center_x':0.5}
                text:'Start chat'
                on_release:root.create_chat()







<RegisterScreen@Screen>:
    sm: app.sm
    capture: app.capture
    BoxLayout:
        orientation:'vertical'
        Toolbar:
            title: 'Create new account'
            elevation: 8
            background_palette: 'Primary'
            md_bg_color: app.theme_cls.primary_color
            background_hue: '500'
        ScrollView:
            do_scroll_x:False
            BoxLayout:
                orientation:'vertical'
                padding:27
                spacing:12
                size_hint_y:None
                height:self.minimum_height
                MDTextField:
                    hint_text:'Enter nickname'
                    id:nick
                    helper_text_mode: "on_error"
                    required:True
                    max_text_length: 32
                    on_text:root.check('nick')
                MDTextField:
                    required: True
                    hint_text:'Enter ID'
                    id:id
                    max_text_length: 32
                    helper_text_mode: "on_error"
                    on_text:root.check('id')
                MDTextField:
                    hint_text:'Enter password'
                    id:passw
                    password:True
                    max_text_length: 32
                    helper_text_mode: "on_error"
                    required: True
                    on_text:root.check('passw')
                MDLabel:
                    font_style:'Title'
                    halign:'center'
                    theme_text_color: 'Custom'
                    text:'Password strengh: '
                    id:strength
                    text_color: 1,1,1,1
                    markup: True
                    size_hint_y:None
                    height:self.texture_size[1]
                MDTextField:
                    id:repeat
                    password:True
                    hint_text:'Repeat password'
                    helper_text_mode: 'on_error'
                    required: True
                MDRaisedButton:
                    pos_hint:{'center_x':0.5}
                    text:'Sign up'
                    id:sign_up
                    disabled: nick.text == '' or id.text == '' or passw.text == '' or repeat.text == '' or repeat.text != passw.text
                    on_release:root.register()



<HelloScreen@Screen>:
    sm:app.sm
    BoxLayout:
        orientation:'vertical'
        padding:20
        AnchorLayout:
            anchor_y:'center'
            anchor_x:'center'
            BoxLayout:
                orientation:'vertical'
                spacing:20
                size_hint_y:None
                height:self.minimum_height
                Image:
                    source:'logo.png'
                    pos_hint:{'center_x':0.5}
                    size_hint_y:None
                    height:self.texture_size[1]
        AnchorLayout:
            anchor_y:'bottom'
            anchor_x:'center'
            BoxLayout:
                orientation:'vertical'
                spacing:20
                size_hint_y:None
                height:self.minimum_height
                MDRaisedButton:
                    text:'sign up'
                    pos_hint:{'center_x':0.5}
                    on_release:app.sm.current='register'


<ContactsScreen@Screen>:
    sm: app.sm
    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            title: 'Contacts' if root.online_mode == 1 else 'Offline Mode'
            elevation: 8
            background_palette: 'Primary'
            md_bg_color: app.theme_cls.primary_color
            background_hue: '500'
        BoxLayout:
            orientation: 'vertical'
            FloatLayout:
                BoxLayout:
                    ScrollView:
                        do_scroll_x: False
                        bar_width: 3
                        BoxLayout:
                            id: layout
                            orientation: 'vertical'
                            size_hint: (1, None)
                            height: self.minimum_height

                MDFloatingActionButton:
                    icon: 'plus'
                    elevation_normal: 8
                    on_release: app.sm.transition.direction = 'left'; app.sm.current = 'prepare_new_contact'
                    pos_hint: {'center_x': 0.9, 'center_y': 0.1}

<LoginScreen@Screen>:
    sm: app.sm
    capture: app.capture
    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            title: 'Login'
            elevation: 8
            background_palette: 'Primary'
            md_bg_color: app.theme_cls.primary_color
            background_hue: '500'
        ScrollView:
            do_scroll_x:False
            BoxLayout:
                orientation:'vertical'
                padding:27
                spacing:12
                size_hint_y:None
                height:self.minimum_height
                MDTextField:
                    tries: 3
                    hint_text: 'Enter password'
                    id: passw
                    helper_text_mode: 'on_error'
                    password: True
                MDRaisedButton:
                    pos_hint:{'center_x':0.5}
                    text:'Sign on'
                    id:sign_on
                    on_release:root.login()
                MDFlatButton:
                    pos_hint:{'center_x':0.5}
                    text:'I forgot my password'
                    id:forgot
                    on_release:root.forgot()

<PrepareNewContactScreen@Screen>:
    sm: app.sm
    capture: app.capture
    BoxLayout:
        orientation:'vertical'
        Toolbar:
            title: 'Share contact'
            elevation: 8
            background_palette: 'Primary'
            md_bg_color: app.theme_cls.primary_color
            background_hue: '500'
        ScrollView:
            do_scroll_x:False
            BoxLayout:
                orientation:'vertical'
                padding:27
                spacing:12
                size_hint_y:None
                height:self.minimum_height
                MDLabel:
                    theme_text_color:'Primary'
                    font_style:'Body2'
                    size_hint_y:None
                    text:"Scan partner QR code and show him your QR. You MUST share contacts at the same time! If somebody close and reopen screen with code your encryption keys wouldn't be equal and because of that you couldn't encrypt partner messages"
                    pos_hint:{'center_x':0.5}
                    halign:'center'
                    height:self.texture_size[1]
                MDRaisedButton:
                    id:goto
                    pos_hint:{'center_x':0.5}
                    on_release:self.disabled=True;root.goto()
                    text:'I understand'

'''
Builder.load_string(kv)


'''
WIDGET CLASSES
'''


class CoverImage1(CoverBehavior, Image):
    source = 'cover.jpg'

    def __init__(self, **kwargs):
        super(CoverImage1, self).__init__(**kwargs)
        texture = self._coreimage.texture
        self.reference_size = texture.size
        self.texture = texture


class CoverImage2(CoverBehavior, Image):
    source = 'cover2.jpg'

    def __init__(self, **kwargs):
        super(CoverImage2, self).__init__(**kwargs)
        texture = self._coreimage.texture
        self.reference_size = texture.size
        self.texture = texture


class BottomChatField(BoxLayout):
    pass


class ContactListItem(OneLineListItem):
    chat_id = StringProperty()
    own_chat_id = StringProperty()
    key = StringProperty()
    user_id = StringProperty()
    own_key = StringProperty()
    sm = ObjectProperty()

    def preload(self, *args):
        self.sm.get_screen('chat').chatname = self.text
        self.sm.get_screen('chat').chat_id = self.chat_id
        self.sm.get_screen('chat').own_chat_id = self.own_chat_id
        self.sm.get_screen('chat').user_id = self.user_id
        self.sm.get_screen('chat').key = self.key
        self.sm.get_screen('chat').own_key = self.own_key
        self.sm.get_screen('chat').closed = True
        self.sm.get_screen('chat').load()
        Clock.schedule_once(self.goto, 0.3)

    def goto(self, *args):
        self.sm.transition.direction = 'left'
        self.sm.current = 'chat'


class MessageDialogContent(BoxLayout):
    '''def __init__(self, **kwargs):
        super(MessageDialog, self).__init__(**kwargs)
    '''


class ToMSG(ButtonBehavior, BoxLayout):
    txt = StringProperty()
    msg_id = StringProperty()
    datetime = StringProperty()

    def __init__(self, **kwargs):
        super(ToMSG, self).__init__(**kwargs)
        self.get_links()
        self.bind(on_release=self.open_dialog)

    def get_links(self, *args):
        self.ids.txt.bind(on_ref_press=self.open_web)
        self.ids.txt.text = self.ids.txt.text.replace('[', '&bl;')
        self.ids.txt.text = self.ids.txt.text.replace(']', '&br;')
        self.ids.txt.text = self.ids.txt.text.replace(']', '&amp;')
        links = re.findall(r'(https?://[^\s]+)', self.ids.txt.text)
        for i in links:
            self.ids.txt.text = self.ids.txt.text.replace(i, '[ref='+i+'][color=1565c0]'+i+'[/color][/ref]')

    def open_web(self, *args):
        launch_webbrowser(args[1])

    def open_dialog(self, *a):
        Clipboard.copy(self.ids.txt.text)
        Snackbar('Text was copied to clipboard').show()


class FromMSG(ButtonBehavior, BoxLayout):
    icon = StringProperty('content-save')
    msg_id = StringProperty()
    icon_txt = StringProperty()
    f_size = NumericProperty()
    txt = StringProperty()
    stat = StringProperty(u'\uF150')
    datetime = StringProperty()

    def __init__(self, **kwargs):
        super(FromMSG, self).__init__(**kwargs)
        self.bind(on_release=self.open_dialog)
        self.get_links()

    def get_links(self, *args):
        self.ids.txt.bind(on_ref_press=self.open_web)
        self.ids.txt.text = self.ids.txt.text.replace('[', '&bl;')
        self.ids.txt.text = self.ids.txt.text.replace(']', '&br;')
        self.ids.txt.text = self.ids.txt.text.replace(']', '&amp;')
        links = re.findall(r'(https?://[^\s]+)', self.ids.txt.text)
        for i in links:
            self.ids.txt.text = self.ids.txt.text.replace(i, '[ref='+i+'][color=1565c0]'+i+'[/color][/ref]')

    def open_web(self, *args):
        launch_webbrowser(args[1])

    def open_dialog(self, *args):
        '''
        content = BoxLayout(orientation='vertical', size_hint_y=None)
        content.bind(height=content.setter('minimum_height'))
        copy_txt = MDLabel(
            font_style='Body1',
            theme_text_color='Secondary',
            text='Copy text',
            size_hint_y=None,
            valign='top'
        )
        copy_txt.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(
            title="Message",
            content=copy_txt,
            size_hint=(.5, None),
            height=dp(200)
        )
        self.dialog.open()
        '''
        Clipboard.copy(self.ids.txt.text)
        Snackbar('Text was copied to clipboard').show()

class ZBarCam(AnchorLayout):
    sm = ObjectProperty()
    resolution = ListProperty([640, 480])
    symbols = ListProperty([])
    Qrcode = namedtuple('Qrcode', [
        'type',
        'data',
        'bounds',
        'quality',
        'count'
     ])

    def __init__(self, **kwargs):
        super(ZBarCam, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self._setup())
        # creates a scanner used for detecting qrcode
        self.scanner = zbar.ImageScanner()
        self.sleep = 0
        self.scanner.parse_config('enable')
        # disables every scanning
        self.scanner.set_config(0, zbar.Config.ENABLE, 0)
        # enables qr scanning
        self.scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1)

    def _setup(self, *args):
        self._remove_shoot_button()
        self._enable_android_autofocus()

    def bund(self, *args):
        self.xcamera._camera.bind(on_texture=self._on_texture)

    def _remove_shoot_button(self):
        xcamera = self.xcamera
        shoot_button = xcamera.children[0]
        xcamera.remove_widget(shoot_button)

    def _enable_android_autofocus(self):
        if not self.is_android():
            return
        camera = self.xcamera._camera._android_camera
        params = camera.getParameters()
        params.setFocusMode('continuous-video')
        camera.setParameters(params)

    def _on_texture(self, instance):
        self._detect_qrcode_frame(
            instance=None,
            camera=instance,
            texture=instance.texture
        )

    def _detect_qrcode_frame(self, instance, camera, texture):
        if self.sleep == 60:
            self.sleep = 0
            image_data = texture.pixels
            size = texture.size
            fmt = texture.colorfmt.upper()
            pil_image = PIL.fromstring(mode=fmt, size=size, data=image_data)
            pil_image = pil_image.resize((512, 385), PIL.ANTIALIAS)
            pil_image = pil_image.convert('L')
            pil_image = pil_image.rotate(-90)
            pil_image = pil_image.transpose(PIL.FLIP_LEFT_RIGHT)
            width, height = pil_image.size
            raw_image = pil_image.tostring()
            zimage = zbar.Image(width, height, "Y800", raw_image)
            result = self.scanner.scan(zimage)
            if result == 0:
                self.symbols = []
                return
            else:
                s = ''.join(sym.data for sym in zimage)
                self.sm.get_screen('new_contact').partner_info(s)

        else:
            self.sleep += 1

    @property
    def xcamera(self):
        return self.ids['xcamera']

    def start(self):
        self.xcamera.play = True

    def stop(self):
        self.xcamera.play = False

    def is_android(self):
        return platform == 'android'


class ZBarCamDesktop(Image):
    sm = ObjectProperty()

    def __init__(self, capture, **kwargs):
        super(ZBarCamDesktop, self).__init__(**kwargs)
        self.fps = 10
        self.capture = capture
        self.play = False
        self.scanner = zbar.ImageScanner()
        # disables every scanning
        self.scanner.set_config(0, zbar.Config.ENABLE, 0)
        # enables qr scanning
        self.scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1)

    def update(self, dt):
        import cv2
        from kivy.graphics.texture import Texture
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            pil_image = PIL.frombytes(data=buf1.tobytes(), mode='RGB', size=(frame.shape[1], frame.shape[0]))
            pil_image = pil_image.resize((512, 385), PIL.ANTIALIAS)
            pil_image = pil_image.convert('L')
            pil_image = pil_image.transpose(PIL.FLIP_LEFT_RIGHT)
            width, height = pil_image.size
            raw_image = pil_image.tobytes()
            zimage = zbar.Image(width, height, "Y800", raw_image)
            result = self.scanner.scan(zimage)
            if result == 0:
                self.symbols = []

            else:
                s = ''.join(sym.data for sym in zimage)
                self.sm.get_screen('new_contact').partner_info(s)

            # display image from the texture
            self.texture = image_texture

    def bund(self, *a):
        self.cl = Clock.schedule_interval(self.update, 1.0/self.fps)


class MText(MDLabel):
    pass


'''
SCREEN WIDGETS
'''


def launch_webbrowser(url):
    import webbrowser
    if platform == 'android':
        from jnius import autoclass, cast

        def open_url(url):
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            browserIntent = Intent()
            browserIntent.setAction(Intent.ACTION_VIEW)
            browserIntent.setData(Uri.parse(url))
            currentActivity = cast('android.app.Activity', activity)
            currentActivity.startActivity(browserIntent)

        class AndroidBrowser(object):

            def open(self, url, new=0, autoraise=True):
                open_url(url)

            def open_new(self, url):
                open_url(url)

            def open_new_tab(self, url):
                open_url(url)

        webbrowser.register('android', AndroidBrowser, None, -1)

    webbrowser.open(url)


class PrepareNewContactScreen(Screen):
    sm = ObjectProperty()
    capture = ObjectProperty()

    def goto(self, *args):
        global DB
        self.ids.goto.disabled = True
        self.sm.get_screen('new_contact').qr_gen()
        self.sm.get_screen('new_contact').ids.zbarcam.bund()
        self.sm.get_screen('new_contact').ids.zbarcam.play = True
        self.ids.goto.disabled = False
        self.sm.current = 'new_contact'


class LoginScreen(Screen):
    sm = ObjectProperty()
    deletes = NumericProperty()
    capture = ObjectProperty()

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.backgr_load, 0.1)

    def login(self, *args):
        global DB
        DB = JsonDataBase(self.ids.passw.text)
        if not DB.read() == 'successfull':
            if self.ids.passw.tries > 0:
                self.ids.passw.error = True
                self.ids.passw.helper_text = 'Invalid password. Tries: ' + str(self.ids.passw.tries)
                self.ids.passw.focus = True
                self.ids.passw.tries -= 1
                return
            else:
                # Добавить экран блокировки
                App().stop()
                return
        else:
            self.ids.passw.error = False
            self.ids.passw.helper_text = ''
            self.ids.passw.tries = 3
        data = dumps({'id': DB.user_id, 'key': DB.session_key})
        data = traffic_crypt(data)
        req = UrlRequest(
            url=DOMAIN+'login.php',
            method='POST',
            req_body=urlencode({'data': data}),
            req_headers=HEADER,
            on_success=self.got,
            on_error=self.fail,
            on_failure=self.fail
        )
        self.ids.sign_on.disabled = True
        self.ids.sign_on.text = 'Loading...'

    def got(self, *args):
        global DB
        try:
            resp = loads(traffic_decrypt(args[1]))
        except:
            Snackbar('Server error. Try again later').show()
            self.ids.sign_on.disabled = False
            self.ids.sign_on.text = 'Sign on'
            return
        # if local session key equals key on server
        if resp['login'] == 'confirmed':
            if DB.update_session_key(resp['session_key']) != 'successfull':
                exit(1)

            # open Contacts screen
            self.sm.get_screen('contacts').online_mode = 1
            Clock.schedule_once(self.precreate)

        else:
            self.ids.sign_on.disabled = False
            self.ids.sign_on.text = 'Sign on'
            Snackbar('Invalid session key!').show()

    def fail(self, *args):
        self.ids.sign_on.disabled = False
        self.ids.sign_on.text = 'Sign on'
        self.sm.get_screen('contacts').online_mode = 0
        Clock.schedule_once(self.precreate)

    def backgr_load(self, *args):
        # background loading nex screen
        if 'contacts' not in [i.name for i in self.sm.screens]:
            self.sm.add_widget(ContactsScreen(name='contacts'))

        if 'prepare_new_contact' not in [i.name for i in self.sm.screens]:
            self.sm.add_widget(PrepareNewContactScreen(name='prepare_new_contact'))

        if 'new_contact' not in [i.name for i in self.sm.screens]:
            new_contact_scr = NewContactScreen(name='new_contact')
            if PLATFORM != 'android':
                new_contact_scr.ids.box.add_widget(ZBarCamDesktop(self.capture, pos_hint={'center_x': 0.5}))
                new_contact_scr.ids.zbarcam = new_contact_scr.ids.box.children[0]

            else:
                new_contact_scr.ids.box.add_widget(ZBarCam())
                new_contact_scr.ids.zbarcam = new_contact_scr.ids.box.children[0]
            new_contact_scr.ids.box.add_widget(QRCodeWidget(pos_hint={'center_x': 0.5}, show_border=False))

            if new_contact_scr.ids.box.children[1].__class__.__name__ == 'QRCodeWidget':
                new_contact_scr.ids.qrcode = new_contact_scr.ids.box.children[1]
            else:
                new_contact_scr.ids.qrcode = new_contact_scr.ids.box.children[0]

            self.sm.add_widget(new_contact_scr)
        else:
            new_contact_scr = [i for i in self.sm.screens if i.name == 'new_contact'][0]

    def precreate(self, *args):
        self.sm.get_screen('contacts').create(DB.contacts)
        self.sm.current = 'contacts'

    def forgot(self, *args):
        warning = '''[size=16][color=#d50000]WARNING[/color][/size]\n
If you delete account you [size=14][color=#d50000]CAN\'T RECOVER IT[/color][/size], all your messages, contacts, files.\nSo, if you want to continue just push the button "I\'M SURE" [b]40 times[/b]'''
        content = MDLabel(
            font_style='Body1',
            theme_text_color='Secondary',
            text=warning,
            size_hint_y=None,
            markup=True,
            valign='top'
        )
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(
            title="Delete account",
            content=content,
            size_hint=(.8, None),
            height=dp(300),
            auto_dismiss=False
        )
        self.dialog.add_action_button('I\'m sure',  action=lambda *x: self.delete_accept())
        self.dialog.add_action_button('cancel',  action=lambda *x: self.delete_cancel())
        self.dialog.open()

    def delete_accept(self):
        warning = '''[size=16][color=#d50000]WARNING[/color][/size]\n
If you delete account you [size=14][color=#d50000]CAN\'T RECOVER IT[/color][/size], all your messages, contacts, files.\nSo, if you want to continue just push the button "I\'M SURE" '''
        if self.deletes != 40:
            self.dialog.ids.container.children[0].text = warning + '[b]' + str(40 - self.deletes) + ' times[/b]'
            self.deletes += 1
        else:
            # because user can make more than 40 pushes and system'll try to delete the file again. It won't find the file and will throw an exception
            try:
                os.remove('db.json')
                self.dialog.dismiss()
                Snackbar('Account was deleted').show()
                self.sm.add_widget(HelloScreen(name='hello'))
                self.sm.add_widget(RegisterScreen(name='register'))
                self.sm.current = 'hello'
            except:
                pass

    def delete_cancel(self):
        self.deletes = 0
        self.dialog.dismiss()


class NewContactScreen(Screen):
    sm = ObjectProperty()

    def qr_gen(self, *args):
        global DB
        self.chat_key = key_gen()
        if platform == 'android':
            self.ids.zbarcam.xcamera.play = True
        self.nick = DB.nick
        self.user_id = DB.user_id
        # It's dangerous in the future
        self.own_chat_id = sha1(self.user_id + str(randint(-9999999, 9999999))).hexdigest()
        data = b64encode(dumps({
            'chat_key': self.chat_key,
            'nickname': self.nick.encode('utf-8'),
            'id': self.user_id,
            'chat_id': self.own_chat_id
        }))
        self.ids.qrcode.data = data

    def go_back(self, *args):
        if PLATFORM == 'android':
            self.ids.zbarcam.xcamera.play = False
            self.ids.zbarcam.ids.xcamera.unbind()
        else:
            Clock.unschedule(self.ids.zbarcam.cl)
        self.sm.transition.direction = 'right'
        self.sm.current = 'contacts'

    def partner_info(self, *args):
        global DB
        partner_data = loads(b64decode(args[0]))
        if partner_data['id'] not in DB.contacts.keys():
            DB.contacts[partner_data['id']] = {
                'key': partner_data['chat_key'],
                'nick': partner_data['nickname'],
                'chat_id': partner_data['chat_id'],
                'own_chat_id': self.own_chat_id,
                'own_key': self.chat_key
            }
            # save encoded data on device
            DB.write()
            Snackbar(partner_data['nickname']+' was added to contacts').show()
            self.sm.get_screen('contacts').create(DB.contacts)

        else:
            pass


class ChatScreen(Screen):
    global DB
    sm = ObjectProperty()
    chatname = StringProperty()
    chat_id = StringProperty()
    own_chat_id = StringProperty()
    user_id = StringProperty()
    own_key = StringProperty()
    key = StringProperty()
    closed = False

    def get_cached_msg(self, *args):
        self.ids.msg.clear_widgets()
        if self.chat_id in DB.chats.keys():
            self.ids.frame.remove_widget(self.ids.create_chat)
            if len(self.ids.frame.children) == 1:
                self.ids.frame.add_widget(BottomChatField())

            for i in DB.chats[self.chat_id]['main_chain']:
                if 'from' in i.keys():
                    # print('To', i['msg'])
                    msg = loads(i['msg'])
                    if msg['type'] == 'txt':
                        self.ids.msg.add_widget(ToMSG(
                            txt=str(msg['text']),
                            msg_id=i['msg_id'],
                            datetime=i['date']
                        ))

                else:
                    # print('FRom', i['msg'])
                    msg = loads(i['msg'])
                    if msg['type'] == 'txt':
                        self.ids.msg.add_widget(FromMSG(txt=msg['text'], msg_id=i['msg_id'], datetime=msg['date'].split(';')[0], stat=u'\uF12C'))

            for i in DB.chats[self.chat_id]['sending_chain']:
                msg = loads(i['msg'])
                if msg['type'] == 'txt':
                    self.ids.msg.add_widget(FromMSG(
                                txt=msg['text'],
                                datetime=msg['date'].split(';')[0],
                                msg_id=i['msg_id'],
                                stat=u'\uF150')
                    )

        else:
            pass
        self.ids.scroll.scroll_y = 0

    def sndmsg(self, msg, tpe, *args):
        if self.ids.frame.children[0].__class__.__name__ == 'BottomChatField':
            self.ids.frame.children[0].ids.message.text = ''
        else:
            self.ids.frame.children[1].ids.message.text = ''

        msg = msg.replace('\n', ' ')
        raw_txt = msg
        msg_id = sha1(b64encode(dumps(
            {
                'type': 'txt',
                'date': ctime() + ';' + str(timezone),
                'text': b64encode(msg.encode('utf-8'))
            }
        ))).hexdigest()
        # print(len(b64decode(self.own_key)))

        msg = '<' + AESCipher(b64decode(self.own_key)).encrypt(dumps({'type': 'txt', 'date': ctime() + ';' + str(timezone), 'text': msg, 'msg_id': msg_id})) + '>'
        # add msg to sending chain
        tr = DB.append_snd_msg(self.chat_id, msg_id, dumps({'type': 'txt', 'date': ctime() + ';' + str(timezone), 'text': raw_txt, 'msg_id': msg_id}))
        self.user_id = DB.user_id
        self.session_key = DB.session_key
        data = dumps({
            'msg': msg,
            'chat_id': self.own_chat_id,
            'id': self.user_id,
            'key': self.session_key,
            'msg_id': msg_id
        })
        data = traffic_crypt(data)
        req = UrlRequest(
            url=DOMAIN+'sndmsg.php',
            method='POST',
            req_body=urlencode({'data': data}),
            req_headers=HEADER,
            on_success=self.sent,
            on_error=self.fail,
            on_failure=self.fail
        )
        '''
        add a message to ChatScreen with status 'Sending...' and msg_id is a unique(not so unique, fix it later) ID hashed with SHA1
        '''
        self.ids.msg.add_widget(FromMSG(txt=raw_txt, msg_id=msg_id, datetime=ctime(), stat=u'\uF150'))

    def resendmsg(self, *a):
        if self.chat_id not in DB.chats.keys():
            return
        for i in DB.chats[self.chat_id]['sending_chain']:
            msg = loads(i['msg'])
            msg_id = msg['msg_id']
            msg = '<' + AESCipher(b64decode(self.own_key)).encrypt(dumps({'type': 'txt', 'date': ctime() + ';' + str(timezone), 'text': msg, 'msg_id': msg_id})) + '>'
            self.user_id = DB.user_id
            self.session_key = DB.session_key
            data = dumps({
                'msg': msg,
                'chat_id': self.own_chat_id,
                'id': self.user_id,
                'key': self.session_key,
                'msg_id': msg_id
            })
            data = traffic_crypt(data)
            req = UrlRequest(
                url=DOMAIN+'sndmsg.php',
                method='POST',
                req_body=urlencode({'data': data}),
                req_headers=HEADER,
                on_success=self.sent,
                on_error=self.fail,
                on_failure=self.fail
            )


    def getmsg(self, *args):
        self.user_id = DB.user_id
        self.session_key = DB.session_key
        data = dumps({
            'chat_id': self.chat_id,
            'id': self.user_id,
            'key': self.session_key
        })
        data = traffic_crypt(data)
        req = UrlRequest(
            url=DOMAIN+'getmsg.php',
            method='POST',
            req_body=urlencode({'data': data}),
            req_headers=HEADER,
            on_success=self.got,
            on_error=self.got_f,
            on_failure=self.got_f
        )

    def got(self, *args):
        played = False
        try:
            resp = loads(traffic_decrypt(args[1]))
        except:
            Snackbar('Server error. Try again later').show()
            return
        # на случай, если чат ещё не создан, а сообщение уже пришло
        if self.chat_id not in DB.chats.keys():
            self.create_chat()
        if resp['getting_msg'] == 'successfull':
            for msg in re.findall(r'<[a-z | A-Z | 0-9 | \+ | / | =]+>', resp['msg']):
                if AESCipher(b64decode(self.key)).decrypt(msg) != '':
                    self.hashed_msgs = resp['msg']
                    msg = loads(AESCipher(b64decode(self.key)).decrypt(msg))
                    raw_msg = dumps(msg)
                    tr = DB.append_got_msg(self.chat_id, msg['msg_id'], raw_msg, msg['date'])
                    if tr != 'error':
                        if msg['type'] == 'txt':
                            # print(msg['text'], msg['date'])
                            if not played and PLATFORM != 'android':
                                sound = SoundLoader().load('new_msg.mp3')
                                sound.play()
                                played = True

                            self.ids.msg.add_widget(ToMSG(txt=str(msg['text']), datetime=msg['date'].split(';')[0]))
                    # else:
                        # Logger.error('why')

            self.accept_msg()
            self.ids.scroll.scroll_y = 0

        if (self.closed) and (self.sm.get_screen('contacts').online_mode == 1):
            Clock.schedule_once(self.getmsg)
            Clock.schedule_once(self.resendmsg)
            

    def got_f(self, *args):
        if self.closed:
            self.getmsg()
            self.resendmsg()

    def sent(self, *args):
        try:
            resp = loads(traffic_decrypt(args[1]))
        except:
            Snackbar('Server error. Try again later').show()
            return

        if resp['send'] == 'successfull':
            msg_id = resp['msg_id']
            tr = DB.append_sent_msg(self.chat_id, msg_id)
            for i in self.ids.msg.children:
                if i.msg_id == msg_id:
                    i.stat = u'\uF12C'

    def fail(self, *args):
        pass

    def exit(self, *args):
        self.closed = False
        self.ids.msg.clear_widgets()
        self.sm.transition.direction = 'right'
        self.sm.current = 'contacts'

    def accept_msg(self, *args):
        hashed_msgs = md5(self.hashed_msgs).hexdigest()
        data = dumps({
            'hashed_msgs': hashed_msgs,
            'chat_id': self.chat_id,
            'id': self.user_id,
            'key': self.session_key
        })
        data = traffic_crypt(data)
        req = UrlRequest(
            url=DOMAIN+'acptmsg.php',
            method='POST',
            req_body=urlencode({'data': data}),
            req_headers=HEADER,
            on_success=self.acptd,
            on_error=self.fail,
            on_failure=self.fail
        )

    def acptd(self, *args):
        if traffic_decrypt(args[1]):
            try:
                resp = loads(traffic_decrypt(args[1]))
            except:
                Snackbar('Server error. Try again later').show()
                return
            if resp['accepting'] == 'successfull':
                # Logger.error('alright!')
                pass

    def create_chat(self, *args):
        '''
        /*
        Просто добавляем нового юзера в chats и включаем возможность отправлять сообщения
        */
        '''
        DB.create_chat(self.chat_id)
        if 'BottomChatField' not in [i.__class__.__name__ for i in self.ids.frame.children]:
            self.ids.frame.remove_widget(self.ids.create_chat)
            self.ids.frame.add_widget(BottomChatField())

    def load(self, *args):
        Clock.schedule_once(self.get_cached_msg, 0.01)
        if (self.sm.get_screen('contacts').online_mode == 1) and (self.closed):
            Clock.schedule_once(self.getmsg)
            Clock.schedule_interval(self.resendmsg, 3)

    def account_funcs(self, *args):
        content = BoxLayout(orientation='vertical', size_hint_y=None)
        content.bind(height=content.setter('minimum_height'))
        copy_txt = MDLabel(
            font_style='Body1',
            theme_text_color='Secondary',
            text='Delete chat',
            size_hint_y=None,
            valign='top'
        )
        copy_txt.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(
            title="Chat actions",
            content=copy_txt,
            size_hint=(.5, None),
            height=dp(200)
        )
        self.dialog.open()

    def delete_chat(self, *a):
        pass
        


class RegisterScreen(Screen):
    sm = ObjectProperty()
    capture = ObjectProperty()

    def register(self, *args):
        self.user_id = md5(b64encode(self.ids.id.text.encode('utf-8'))).hexdigest()
        data = dumps({'id': self.user_id})
        # ecnrypt user data and send it to the server
        data = traffic_crypt(data)
        req = UrlRequest(
            url=DOMAIN+'register.php',
            method='POST',
            req_body=urlencode({'data': data}),
            req_headers=HEADER,
            on_success=self.got,
            on_error=self.error,
            on_failure=self.fail
        )
        Clock.schedule_once(self.backgr_load, 0.01)
        self.ids.sign_up.disabled = True
        self.ids.sign_up.text = 'Loading'

    def got(self, *args):
        global DB
        # getting answer from server:dictionary
        try:
            resp = loads(traffic_decrypt(args[1]))
        except:
            Snackbar('Server error. Try again later').show()
            self.ids.sign_up.disabled = False
            self.ids.sign_up.text = 'Sign up'
            return
        if resp['registration'] == 'complete':
            self.session_key = resp['session_key']
            DB = JsonDataBase(self.ids.passw.text)
            DB.create_db(
                self.ids.nick.text,
                self.user_id,
                self.session_key,
                {},
                {},
                {'proxy': '', 'lang': 'ru'},
            )
            # open Contacts screen
            Clock.schedule_once(self.precreate)

        else:
            self.ids.sign_up.disabled = False
            self.ids.sign_up.text = 'Sign up'
            self.ids.id.error = True
            self.ids.id.focus = True
            self.ids.id.helper_text = 'This user already exists'

    def check(self, *args):
        if len(args) != 0:
            if args[0] == 'nick':
                if self.ids.nick.text != '':
                    pass

            if args[0] == 'passw':
                self.passwd_strength()
                if self.ids.nick.text != '':
                    pass

            if args[0] == 'repeat':
                if self.ids.repeat.text != '':
                    if self.ids.repeat.text != self.ids.passw.text:
                        self.ids.repeat.error = True
                        self.ids.repeat.helper_text = 'Passwords aren\'t equal'
                    else:
                        self.ids.repeat.error = False

            if args[0] == 'code':
                if self.ids.nick.text != '':
                    pass

    def backgr_load(self, *args):
        if 'contacts' not in [i.name for i in self.sm.screens]:
            self.sm.add_widget(ContactsScreen(name='contacts'))

        if 'prepare_new_contact' not in [i.name for i in self.sm.screens]:
            self.sm.add_widget(PrepareNewContactScreen(name='prepare_new_contact'))

        if 'new_contact' not in [i.name for i in self.sm.screens]:
            new_contact_scr = NewContactScreen(name='new_contact')
            if PLATFORM != 'android':
                new_contact_scr.ids.box.add_widget(ZBarCamDesktop(self.capture, pos_hint={'center_x': 0.5}))
                new_contact_scr.ids.zbarcam = new_contact_scr.ids.box.children[0]

            else:
                new_contact_scr.ids.box.add_widget(ZBarCam())
                new_contact_scr.ids.zbarcam = new_contact_scr.ids.box.children[0]
            new_contact_scr.ids.box.add_widget(QRCodeWidget(pos_hint={'center_x': 0.5}, show_border=False))

            if new_contact_scr.ids.box.children[1].__class__.__name__ == 'QRCodeWidget':
                new_contact_scr.ids.qrcode = new_contact_scr.ids.box.children[1]
            else:
                new_contact_scr.ids.qrcode = new_contact_scr.ids.box.children[0]

            self.sm.add_widget(new_contact_scr)
        else:
            new_contact_scr = [i for i in self.sm.screens if i.name == 'new_contact'][0]

    def precreate(self, *args):
        self.sm.get_screen('contacts').create({})
        self.sm.get_screen('contacts').online_mode = 1
        self.sm.current = 'contacts'

    def error(self, *a):
        # print('error', a)
        Snackbar('Error occurred').show()
        self.ids.sign_up.disabled = False
        self.ids.sign_up.text = 'Sign up'

    def fail(self, *a):
        # print('fail', a)
        Snackbar('Error occurred').show()
        self.ids.sign_up.disabled = False
        self.ids.sign_up.text = 'Sign up'

    def exit(self, *a):
        self.ids.passw.text = ''
        self.ids.nick.text = ''
        self.ids.id.text = ''
        self.ids.repeat.text = ''
        self.sm.current = 'hello'

    def passwd_strength(self, *a):
        symbols = ['/', '.', '*', ';', ',', '\\', '"', '\'', '#', '@', ':', '?', '!', '$', '^', '&', '(', ')', '=', '+', '%', '<', '>']
        low_case = [chr(i) for i in range(97, 123)]
        upper_case = [chr(i) for i in range(65, 91)]
        numbers = [chr(i) for i in range(49, 58)]
        dct_symbs = {'nums': 0, 'low': 0, 'upper': 0, 'symbs': 0, 'len': len(self.ids.passw.text)}
        for i in self.ids.passw.text:
            if i in low_case:
                dct_symbs['low'] += 1
            if i in upper_case:
                dct_symbs['upper'] += 1
            if i in numbers:
                dct_symbs['nums'] += 1
            if i in symbols:
                dct_symbs['symbs'] += 1
        res = '[color='
        if dct_symbs['len'] >= 14:
            if dct_symbs['upper'] + dct_symbs['low'] + dct_symbs['symbs'] + dct_symbs['nums'] >= 3:
                res += '#64dd17]Best'
        elif dct_symbs['len'] >= 8:
            if dct_symbs['upper'] + dct_symbs['low'] + dct_symbs['symbs'] + dct_symbs['nums'] >= 3:
                res += '#9ccc65]Strong'
            elif dct_symbs['upper'] + dct_symbs['low'] + dct_symbs['symbs'] + dct_symbs['nums'] >= 2:
                res += '#ffd600]Medium'
        elif dct_symbs['upper'] and dct_symbs['low'] and dct_symbs['symbs'] and dct_symbs['nums']:
            res += '#c0392b]Weak'
        else:
            res += '#d50000]Not a password'
        res += '[/color]'
        self.ids.strength.text = 'Password strength: ' + res


class ContactsScreen(Screen):
    online_mode = NumericProperty(0)
    contacts = ListProperty()
    sm = ObjectProperty()
    loaded = NumericProperty(0)

    def create(self, *args):
        Clock.schedule_once(self.backgr_load, 0.5)
        if 'login' in [i.name for i in self.sm.screens]:
            self.sm.remove_widget(self.sm.get_screen('login'))

        if 'register' in [i.name for i in self.sm.screens]:
            self.sm.remove_widget(self.sm.get_screen('register'))

        self.ids.layout.clear_widgets()
        if args[0] and args[0] != ['']:
            for i in args[0].items():
                self.ids.layout.add_widget(ContactListItem(
                    text=i[1]['nick'],
                    chat_id=i[1]['chat_id'],
                    own_chat_id=i[1]['own_chat_id'],
                    user_id=i[0],
                    key=i[1]['key'],
                    own_key=i[1]['own_key']
                ))
        else:
            self.ids.layout.add_widget(MText(text='No contacts yet', halign='center', font_style='Subhead'))

    def backgr_load(self, *args):
        if not bool(self.loaded):
            self.sm.add_widget(ChatScreen(name='chat'))
            self.loaded = 1


class HelloScreen(Screen):
    pass
    '''def an(self,*args):
        self.ids.logo.y=Window.height/4*3
        anim=Animation(opacity=0.95,duration=0.5,t='in_circ')
        anim&=Animation(y=Window.height-100,duration=0.2,t='in_circ')
        anim.repeat=False
        anim.start(self.ids.logo)
    '''


class CryptoChat(App):
    theme_cls = ThemeManager()
    session_key = ''
    theme_cls.primary_palette = 'BlueGrey'
    theme_cls.accent_palette = 'Grey'
    theme_cls.theme_style = 'Dark'
    sm = ScreenManager()
    config_parser = ConfigParser()

    def build(self):
        Window.bind(on_keyboard=self.events)
        self.theme_cls.bind(primary_palette=lambda x, y: self.theme_changed(x, y, 'primary'))
        self.theme_cls.bind(accent_palette=lambda x, y: self.theme_changed(x, y, 'accent'))
        self.theme_cls.bind(theme_style=lambda x, y: self.theme_changed(x, y, 'theme_style'))
        if PLATFORM != 'android':
            import cv2
            self.capture = cv2.VideoCapture(0)

        else:
            self.capture = None

        if os.path.exists('db.json'):
            self.sm.add_widget(LoginScreen(name='login'))
            self.sm.current = 'login'

        else:
            self.sm.add_widget(HelloScreen(name='hello'))
            self.sm.add_widget(RegisterScreen(name='register'))
        return self.sm

    def theme_changed(self, *args):
        print(args[1], args[2])


    def events(self, instance, keyboard, keycode, text, modifiers):
        if (keyboard in (27, 1001)) and (self.sm.current == 'new_contact'):
            if PLATFORM != 'android':
                Clock.unschedule(self.sm.get_screen('new_contact').ids.zbarcam.cl)
            self.sm.transition.direction = 'right'
            self.sm.current = 'contacts'

        if (keyboard in (27, 1001)) and (self.sm.current == 'prepare_new_contact'):
            self.sm.transition.direction = 'right'
            self.sm.current = 'contacts'

        if (keyboard in (27, 1001)) and (self.sm.current == 'chat'):
            self.sm.get_screen('chat').exit()
        '''
        #if (keyboard in (27,1001))  and (self.sm.current=='filemanager'):
        #    self.sm.get_screen('filemanager').file_manager.back()
        '''


'''
MAINLOOP
'''


CryptoChat().run()
