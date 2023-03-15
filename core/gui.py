import tkinter as tk
import keyboard
from utils import Singleton, ConfigManager


class Window(tk.Toplevel, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cfg = ConfigManager().get_config()

        self.opened = False
        self.geometry("800x600")
        self.wm_attributes('-topmost', 1)

    def showhide(self):
        cm = ConfigManager()
        cfg = cm.get_config()
        if not self.opened:
            self.deiconify()
            self.geometry("+{}+{}".format(
                cfg['settingswindow']['pos'][0],
                cfg['settingswindow']['pos'][1]
            ))
            self.opened = True
        else:
            cfg['settingswindow']['pos'] = [
                self.winfo_x(),
                self.winfo_y()
            ]
            cm.change_config(cfg)
            self.withdraw()
            self.opened = False


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cfg = ConfigManager().get_config()

        self.geometry("100x150+{}+{}".format(
            cfg['infowindow']['pos'][0],
            cfg['infowindow']['pos'][1]
        ))
        self.overrideredirect(1)
        self.config(bg='black')
        self.wm_attributes('-topmost', 1)
        self.attributes('-transparentcolor', 'black', '-topmost', 1)

        self.titlebar = tk.Frame(self, bg='#282C34', width=100, height=10)
        self.indicators = tk.Label(self, text='NW: \nXPM: \nGPM: ', bg='black', fg='white', font='Alial 10 bold')

        self.titlebar.pack()
        self.indicators.pack()

        self.titlebar.bind('<B1-Motion>', self._move_window)
        keyboard.add_hotkey(cfg['settingswindow']['hotkey'], self.openclose_settings)
        keyboard.add_hotkey(cfg['infowindow']['close_hotkey'], self.destroy)

    def destroy(self) -> None:
        self.update_config()
        return super().destroy()

    def _move_window(self, event):
        self.geometry('+{}+{}'.format(event.x_root, event.y_root))

    def openclose_settings(self):
        window = Window(self)
        window.showhide()

    def on_update_gamestate(self, gamestate):
        self.indicators['text'] = 'Health: {}\nGPM: {}\nXPM: {}'.format(
            gamestate.player.hero.health,
            gamestate.player.gpm,
            gamestate.player.xpm
        )

    def update_config(self):
        cm = ConfigManager()
        cfg = cm.get_config()
        cfg['infowindow']['pos'] = [
            self.winfo_x(),
            self.winfo_y()
        ]

        cm.change_config(cfg)
