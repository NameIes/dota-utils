import os, winreg, vdf, json
from .singleton import Singleton


class ConfigManager(metaclass=Singleton):
    """Using this class, you can get the path to the game, as well as load and save the program settings.

    Raises:
        FileNotFoundError: raises when dota is not installed.
        ValueError: raises when config.json is broken.
    """

    STEAM_REGISTRY_KEY = os.path.join("SOFTWARE", "WOW6432Node", "Valve", "Steam")
    LIBRARY_FOLDERS_PATH = os.path.join("steamapps", "libraryfolders.vdf")
    CLIENT_DLL_PATH = os.path.join("steamapps", "common", "dota 2 beta", "game", "dota", "bin", "win64", "client.dll")
    DOTA_APP_ID = "570"
    APP_MANIFEST_PATH = os.path.join("steamapps", f"appmanifest_{DOTA_APP_ID}.acf")
    DOTA_HOTKEYS_PATH = os.path.join(f"{DOTA_APP_ID}", "remote", "cfg", "dotakeys_personal.lst")
    APP_CONFIG_PATH = os.path.join(os.getcwd(), "config.json")

    def __init__(self) -> None:
        self.app_config = None

    def get_steam_path(self) -> str:
        """Finds steam path in registry.

        Returns:
            string: steam path.
        """
        hhkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.STEAM_REGISTRY_KEY)
        steam_path = winreg.QueryValueEx(hhkey, "InstallPath")[0]
        winreg.CloseKey(hhkey)

        return steam_path

    def get_steam_lib_path(self) -> str:
        """Finds library folder with dota, because steam and dota may be storage in different paths.

        Raises:
            FileNotFoundError: raises when dota is not installed.

        Returns:
            string: steam library path.
        """
        lib_folders_path = os.path.join(self.get_steam_path(), self.LIBRARY_FOLDERS_PATH)
        lib_folders = vdf.load(open(lib_folders_path))["libraryfolders"]

        for key in lib_folders:
            if self.DOTA_APP_ID in lib_folders[key]["apps"]:
                return lib_folders[key]["path"]

        raise FileNotFoundError("Dota is not installed.")

    def get_clientdll_path(self) -> str:
        """With client.dll can change camera distance.

        Returns:
            string: client.dll path.
        """
        return os.path.join(self.get_steam_lib_path(), self.CLIENT_DLL_PATH)

    def get_app_manifest_path(self) -> str:
        """App manifest file storage information about steam games, like 'is game updating'

        Returns:
            string: appmanifest.acf path.
        """
        return os.path.join(self.get_steam_lib_path(), self.APP_MANIFEST_PATH)

    def get_hotkeys_path(self, dota_userid) -> str:
        """Returns path to file with dota hotkeys for each steam profile by user id.

        Args:
            dota_userid (string): this is not steamid, this id is in the add friend window in dota.

        Returns:
            string: path to file with dota hotkeys.
        """
        return os.path.join(self.get_steam_path(), "userdata", dota_userid, self.DOTA_HOTKEYS_PATH)

    def get_hotkeys(self, dota_userid) -> dict:
        """Reads file with dota hotkeys, and convert him to dictionary.

        Args:
            dota_userid (string): this is not steamid, this id is in the add friend window in dota.

        Returns:
            dict: dictionary with dota hotkeys.
        """
        hotkeys_path = self.get_hotkeys_path(dota_userid)
        hotkeys = vdf.load(open(hotkeys_path))

        return hotkeys

    def load_config(self) -> None:
        """Loading a file with settings config.json.

        Raises:
            ValueError: raises when config.json is broken.
        """
        cfg_file = open(self.APP_CONFIG_PATH, "r")
        cfg = cfg_file.read()
        cfg_file.close()

        try:
            self.app_config = json.loads(cfg)
        except json.decoder.JSONDecodeError:
            raise ValueError("Config file is broken.")

    def save_config(self) -> None:
        """Saving configuration to config.json."""
        with open(self.APP_CONFIG_PATH, "w") as cfg_file:
            cfg_file.write(json.dumps(self.app_config))

    def get_config(self) -> dict:
        """Returns class attribute with configuration.

        Returns:
            dict: dictionary with config.

        Raises:
            ValueError: raises when config has not been loaded.
        """
        if self.app_config is not None:
            return self.app_config
        raise ValueError("Config file is broken.")

    def change_config(self, data) -> None:
        """Writes data to class attribute.

        Args:
            data (dict): dictionary with config.
        """
        self.app_config = data
