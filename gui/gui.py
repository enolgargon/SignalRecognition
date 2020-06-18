import json
from datetime import datetime, timedelta
from tkinter import *

import requests
from PIL import Image, ImageTk

width, height = 600, 400


class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.center_frame = Frame(root, width=width, height=.9 * height, bg='grey')
        self.center_frame.grid(row=0, column=0, padx=2, pady=2)
        self.bottom_frame = Frame(root, width=width, height=.1 * height, bg='grey')
        self.bottom_frame.grid(row=1, column=0, padx=2, pady=2)

        self.capture = None
        self.images = []
        self.loaded_images = []
        self.lbl_capture = None
        self.lbl_images = []
        self.next_update = datetime.now()

        self.update_images()

    def check_update(self, event):
        if datetime.now() > self.next_update:
            self.update_images()

    def update_images(self):
        print("a")
        try:
            signals, frame = App.request()
            if signals is not '':
                self.images = signals
            if frame is not '':
                self.capture = frame
        except:
            print("bad request()")

        if self.capture is not None:
            render = ImageTk.PhotoImage(Image.open(self.capture).resize((width, int(.9 * height)), Image.ANTIALIAS))
            if self.lbl_capture is None:
                self.lbl_capture = Label(self.center_frame, image=render).grid(row=0, column=0, padx=0, pady=0)
            else:
                self.lbl_capture.configure(image=render)
        self.lbl_images = []
        self.loaded_images = []
        size = int(.1 * height)
        for i in range(len(self.images)):
            self.loaded_images += [ImageTk.PhotoImage(
                Image.open(f'/home/recognition/SignalRecognition/install/icon/{self.images[i]:02d}.png').resize((size, size),
                                                                                     Image.ANTIALIAS))]
            self.lbl_images += [Label(self.bottom_frame, image=self.loaded_images[i])]
            self.lbl_images[i].grid(row=0, column=i, padx=1, pady=1)

        self.next_update = datetime.now() + timedelta(milliseconds=500)
        # self.master.after(500, self.update_images)
        # self.mainloop() # Si pongo esto funciona pero falla al minuto

    @staticmethod
    def request():
        try:
            signals = frame = ''
            response = requests.get('http://127.0.0.1:5000/current-signals')
            if response.status_code == 200:
                signals = [signal['code'] for signal in json.loads(response.content)]

            response = requests.get('http://127.0.0.1:5000/current-frame')
            if response.status_code == 200:
                frame = json.loads(response.content)['frame']
                if frame is None or frame == 'None':
                    frame = ''
                else:
                    frame = f"/home/recognition/images/{frame}.png"
            return signals, frame
        except Exception as e:
            print(f"Error request gui: {e}")
        return None


root = Tk()
app = App(root)
root.wm_title("Tkinter window")
root.bind('<Configure>', app.check_update)
root.geometry(f"{width}x{height}")
root.mainloop()
