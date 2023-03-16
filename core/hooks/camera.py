import struct, re
import tkinter as tk
from .basehook import BaseHook
from utils import ConfigManager


class Camera(BaseHook):
    CAMERA_DISTANCE_HEX = "0000000000002e400000964400006145"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config_manager = ConfigManager()

        tk.Label(self, text="Setup custom camera distance.", bg="#2C313A", fg="white").grid(row=0, column=0, sticky="w")
        tk.Label(self, text="Possible to get banned.", bg="#2C313A", fg="#EB4C42").grid(row=1, column=0, sticky="w")
        tk.Label(self, text="Camera distance restores to default 1200 after update.", bg="#2C313A", fg="white").grid(
            row=2, column=0, sticky="w"
        )
        self.slider = tk.Scale(
            self,
            orient="horizontal",
            from_=1200,
            to=2000,
            bg="#2C313A",
            highlightthickness=0,
            fg="white",
        )
        self.slider.grid(row=3, column=0, sticky="we")
        self.slider.set(self.config_manager.get_config()['hooks']['camera']['installed_distance'])
        tk.Button(self, text="Set distance", bg="#1B8DD1", fg="white", borderwidth=0, command=self.set_distance).grid(
            row=4, column=0, sticky="we", pady=4
        )
        self.err_label = tk.Label(self, text="", bg="#2C313A", fg="#EB4C42").grid(row=5, column=0, sticky="w")

    def _get_data_for_change(self, distance):
        default_distance_hex = struct.pack("f", float(distance)).hex()

        distance_hex = struct.pack("f", float(self.slider.get())).hex()
        distance_hex_length = len(distance_hex)
        distance_index = self.CAMERA_DISTANCE_HEX.find(default_distance_hex)

        hex_string_regex = re.compile(
            self.CAMERA_DISTANCE_HEX[:distance_index]
            + f"\w{{{distance_hex_length}}}"
            + self.CAMERA_DISTANCE_HEX[distance_index + distance_hex_length:]
        )

        distance_hex_string = (
            self.CAMERA_DISTANCE_HEX[:distance_index]
            + distance_hex
            + self.CAMERA_DISTANCE_HEX[distance_index + distance_hex_length:]
        )

        return hex_string_regex, distance_hex_string

    def set_distance(self):
        with open(self.config_manager.get_clientdll_path(), "rb") as f:
            client_dll_hex = f.read().hex()

        hex_string_regex, distance_hex_string = self._get_data_for_change(1200)
        hex_string_regex_cfg, distance_hex_string_cfg = self._get_data_for_change(
            self.config_manager.get_config()['hooks']['camera']['installed_distance']
        )

        if re.search(hex_string_regex_cfg, client_dll_hex) is not None:
            hex_string_regex = hex_string_regex_cfg
            distance_hex_string = distance_hex_string_cfg

        client_dll_hex_new, changes_count = re.subn(
            hex_string_regex, distance_hex_string, client_dll_hex, 1
        )

        if changes_count == 0:
            self.err_label['text'] = "Unable to find distance inside client.dll"
            return

        with open(self.config_manager.get_clientdll_path(), "wb") as f:
            f.write(bytes.fromhex(client_dll_hex_new))

        cfg = self.config_manager.get_config()
        cfg['hooks']['camera']['installed_distance'] = self.slider.get()
