import os, winreg, vdf, json
from .singleton import Singleton


class ConfigManager(metaclass=Singleton):
    STEAM_REGISTRY_KEY = os.path.join("SOFTWARE", "WOW6432Node", "Valve", "Steam")
    LIBRARY_FOLDERS_PATH = os.path.join("steamapps", "libraryfolders.vdf")
    CLIENT_DLL_PATH = os.path.join("steamapps", "common", "dota 2 beta", "game", "dota", "bin", "win64", "client.dll")
    DOTA_APP_ID = "570"
    APP_MANIFEST_PATH = os.path.join("steamapps", f"appmanifest_{DOTA_APP_ID}.acf")
    DOTA_HOTKEYS_PATH = os.path.join(f'{DOTA_APP_ID}', 'remote', 'cfg', 'dotakeys_personal.lst')
    APP_CONFIG_PATH = os.path.join(os.getcwd(), 'config.json')
    def __init__(self) -> None:
        self.app_config = None

    def get_steam_path(self):
        hhkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.STEAM_REGISTRY_KEY)
        steam_path = winreg.QueryValueEx(hhkey, "InstallPath")[0]
        winreg.CloseKey(hhkey)

        return steam_path

    def get_steam_lib_path(self):
        lib_folders_path = os.path.join(self.get_steam_path(), self.LIBRARY_FOLDERS_PATH)
        lib_folders = vdf.load(open(lib_folders_path))['libraryfolders']

        for key in lib_folders:
            if self.DOTA_APP_ID in lib_folders[key]['apps']:
                return lib_folders[key]['path']

        raise FileNotFoundError('Dota is not installed.')

    def get_clientdll_path(self):
        return os.path.join(self.get_steam_lib_path(), self.CLIENT_DLL_PATH)

    def get_app_manifest_path(self):
        return os.path.join(self.get_steam_lib_path(), self.APP_MANIFEST_PATH)

    def get_hotkeys_path(self, dota_userid):
        return os.path.join(self.get_steam_path(), 'userdata', dota_userid, self.DOTA_HOTKEYS_PATH)

    def get_hotkeys(self, dota_userid):
        hotkeys_path = self.get_hotkeys_path(dota_userid)
        hotkeys = vdf.load(open(hotkeys_path))

        return hotkeys

    def load_config(self):
        if self.app_config is not None:
            return self.app_config

        cfg_file = open(self.APP_CONFIG_PATH, 'r')
        cfg = cfg_file.read()
        cfg_file.close()

        try:
            cfg = json.loads(cfg)
        except json.decoder.JSONDecodeError:
            raise ValueError('Config file is broken.')

        self.app_config = cfg

    def save_config(self):
        with open(self.APP_CONFIG_PATH, 'w') as cfg_file:
            cfg_file.write(
                json.dumps(self.app_config)
            )

    def get_config(self):
        return self.app_config

    def change_config(self, data):
        self.app_config = data


if __name__ == "__main__":
    cm = ConfigManager()
    print(cm.load_config())
