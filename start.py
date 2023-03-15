from core.server import get_server
from core.gui import GUI
import threading
from utils import ConfigManager


if __name__ == "__main__":
    config_manager = ConfigManager()
    config_manager.load_config()
    server = get_server()
    gui = GUI()
    server.gamestate.on_update(gui.on_update_gamestate)
    thread = threading.Thread(None, server.run)
    thread.start()
    gui.mainloop()
    server.shutdown()
    thread.join()
    config_manager.save_config()
