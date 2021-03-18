from __future__ import unicode_literals
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.uix.camera import Camera
from kivy.uix.filechooser import FileChooserListView
import time

Builder.load_string("""
<RoundSquare@Button>:
    background_color: 0,0,0,0  
    color: 1,1,0,1
    size: 150,150
    font_size: 60
    text_size: self.size
    halign: 'center'
    valign: 'bottom'
    canvas.before:
        Color:
            rgba: [0.3, 2.7, 0.3, 1] if self.state=='normal' else (0,.7,.7,1)  # visual feedback of press
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [25,]
 
<MainPage>:
    canvas.before:
        Rectangle:
            source: 'plantimage.jpg'
            pos: self.pos
            size: self.size
    FloatLayout:
        RoundSquare:
            text: 'Auto Detect'
            on_release: root.manager.current = 'detect'
            size_hint: 0.35,0.35/2
            pos_hint: {'top':0.80,'right':0.45}
            Image:
            	source: 'cameraicon.png'
            	size: 300,290
            	x: self.parent.x+self.parent.width-330
            	y: self.parent.y+self.parent.height-300
            	allow_stretch: True
        RoundSquare:
            text: 'Manual Input'
            on_release: root.manager.current = 'manual'
            size_hint: 0.35,0.35/2
            pos_hint: {'top':0.80,'right':0.90}
            Image:
                source: 'paperwrite.png'
            	size: 300,290
            	x: self.parent.x+self.parent.width-325
            	y: self.parent.y+self.parent.height-300
            	allow_stretch: True
        RoundSquare:
            text: 'Help'
            on_release: root.manager.current = 'help'
            size_hint: 0.35,0.35/2
            pos_hint: {'top':0.40,'right':0.45}
            Image:
                source: 'questionmark.png'
            	size: 300,290
            	x: self.parent.x+self.parent.width-330
            	y: self.parent.y+self.parent.height-300
            	allow_stretch: True
        RoundSquare:
            text: 'Exit'
            on_release: app.stop()
            size_hint: 0.35,0.35/2
            pos_hint: {'top':0.40,'right':0.90}
            Image:
                source: 'exitimage.png'
            	size: 300,290
            	x: self.parent.x+self.parent.width-330
            	y: self.parent.y+self.parent.height-300
            	allow_stretch: True
<DetectPage>:
    BoxLayout:
        orientation: 'vertical'
        Camera:
            id: camera
            resolution: (640, 480)
            play: False
        ToggleButton:
            text: 'Play'
            on_release: camera.play = not camera.play
            size_hint_y: None
            height: '48dp'
        Button:
            text: 'Capture'
            size_hint_y: None
            height: '48dp'
            on_press: root.capture()
        Button:
            text: 'Main Page'
            size_hint: 1, None
            height: '48dp'
            on_release: root.manager.current = 'main'
""")

class MainPage(Screen):
    pass

class DetectPage(Screen):
    def new_craca(self):
        self.ids['ck_fx01'].color = 1.,1.,1., 1
        self.ids['ck_fx02'].color = 1.,1.,1., 0.6
        self.ids['ck_fx03'].color = 1.,1.,1., 0.6

    def new_ostra(self):
        self.ids['ck_fx01'].color = 1.,1.,1., 0.6
        self.ids['ck_fx02'].color = 1.,1.,1., 1
        self.ids['ck_fx03'].color = 1.,1.,1., 0.6

    def new_alga(self):
        self.ids['ck_fx01'].color = 1.,1.,1., 0.6
        self.ids['ck_fx02'].color = 1.,1.,1., 0.6
        self.ids['ck_fx03'].color = 1.,1.,1., 1

    def reset (self):
        self.ids['msg_error'].text = ''

    def first_capture(self):
        camera=self.ids['camera']
        print (camera.resolution)
        camera.resolution=[640,480]
        return

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        from os import getcwd
        self.cwd = getcwd() + "/"
        path = self.cwd
            return
        from android.permissions import Permission, request_permissions
        request_permissions(Permission.CAMERA)
        global name_trans
        global name_fx
        import os
        camera=self.ids['camera']
        print (camera.resolution)
        camera.resolution=[640,480]

        #if name_trans is not None and  name_fx  is not None  :
        try:
            name_trans and name_fx
            path = str(os.path.abspath(os.path.dirname(__file__)))
            path_faixa = path+"/fotos/%s%s_foto.png"%(name_trans,name_fx)
            if os.path.exists(path_faixa) == True:
                camera = self.ids['camera']
                os.remove(path+"/fotos/%s%s_foto.png"%(name_trans,name_fx))
                camera.export_to_png(path+"/fotos/%s%s_foto.png"%(name_trans,name_fx))
            else:
                camera = self.ids['camera']
                camera.export_to_png(path+"/fotos/%s%s_foto.png"%(name_trans,name_fx))
        except:
            self.ids['msg_error'].text = ''
            self.ids['msg_error'].color = 1,0,0,1
            self.ids['msg_error'].text = 'Selecione o transecto e a faixa!'

                 
class MainApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MainPage(name='main'))
	      sm.add_widget(DetectPage(name='detect'))
        return sm
 
MainApp().run()
