import tkinter as tk
import keyboard
from utils import Singleton, ConfigManager
from core.gamestate import GameState


class SettingsArea(tk.Canvas):
    """Area with pagination buttons and page parameters.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SettingsWindow(tk.Toplevel, metaclass=Singleton):
    """Settings window.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure_window()
        self.configure_widgets()
        self.pack_widgets()
        self.configure_hotkeys()

    def configure_window(self) -> None:
        """Configures window size, position, color...
        """
        self.opened = False
        self.geometry("800x600")
        self.overrideredirect(True)
        self.wm_attributes('-topmost', 1)

    def configure_widgets(self) -> None:
        """Creates widgets and configures its parameters.
        """
        self.titlebar = tk.Frame(self, bg='#282C34', bd=2)
        self.titlelabel = tk.Label(self.titlebar, text='Settings', bg="#282C34", fg='white', width=8, height=1)
        self.settings_area = SettingsArea(self, bg="#2E333C", bd=0, highlightthickness=0)

    def pack_widgets(self) -> None:
        """Places widgets to window.
        """
        self.titlebar.pack(fill=tk.X)
        self.titlelabel.pack(side=tk.TOP)
        self.settings_area.pack(fill=tk.BOTH, expand=1)

    def configure_hotkeys(self) -> None:
        """Setup hotkeys
        """
        self.titlebar.bind('<B1-Motion>', self._move_window)

    def _move_window(self, event):
        """Allows to move window by dragging titlebar.
        """
        self.geometry('+{}+{}'.format(event.x_root, event.y_root))

    def showhide(self):
        """Open self when closed and close when opened.
        """
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


class InfoWindow(tk.Tk):
    """Information window.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        cfg = ConfigManager().get_config()
        self.configure_window(cfg)
        self.configure_widgets()
        self.pack_widgets()
        self.configure_hotkeys(cfg)

    def configure_window(self, cfg: dict) -> None:
        """Configures window size, position, color...

        Args:
            cfg (dict): data from configuration file.
        """
        self.geometry("100x150+{}+{}".format(
            cfg['infowindow']['pos'][0],
            cfg['infowindow']['pos'][1]
        ))
        self.overrideredirect(True)
        self.config(bg='black')
        self.wm_attributes('-topmost', 1)
        self.attributes('-transparentcolor', 'black', '-topmost', 1)

    def configure_widgets(self) -> None:
        """Creates widgets and configures its parameters.
        """
        self.titlebar = tk.Frame(self, bg='#282C34', width=100, height=10)
        self.indicators = tk.Label(self, text='NW: \nXPM: \nGPM: ', bg='black', fg='white', font='Alial 10 bold')

    def pack_widgets(self) -> None:
        """Places widgets to window.
        """
        self.titlebar.pack()
        self.indicators.pack()

    def configure_hotkeys(self, cfg: dict) -> None:
        """Setup hotkeys

        Args:
            cfg (dict): data from configuration file.
        """
        self.titlebar.bind('<B1-Motion>', self._move_window)
        keyboard.add_hotkey(cfg['settingswindow']['hotkey'], self.openclose_settings)
        keyboard.add_hotkey(cfg['infowindow']['close_hotkey'], self.destroy)

    def destroy(self) -> None:
        """Save and close.
        """
        self.update_config()
        super().destroy()

    def _move_window(self, event) -> None:
        """Allows to move window by dragging titlebar.
        """
        self.geometry('+{}+{}'.format(event.x_root, event.y_root))

    def openclose_settings(self) -> None:
        """Open settings window when its closed and close when opened.
        """
        window = SettingsWindow(self)
        window.showhide()

    def on_update_gamestate(self, gamestate: GameState) -> None:
        """This function calls by server when game data updates.

        Args:
            gamestate (GameState): object contains data about game.
        """
        self.indicators['text'] = 'Health: {}\nGPM: {}\nXPM: {}'.format(
            gamestate.player.hero.health,
            gamestate.player.gpm,
            gamestate.player.xpm
        )

    def update_config(self) -> None:
        """Saving window parameters.
        """
        cm = ConfigManager()
        cfg = cm.get_config()
        cfg['infowindow']['pos'] = [
            self.winfo_x(),
            self.winfo_y()
        ]

        cm.change_config(cfg)
