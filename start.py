from core.server import get_server
from core.gui import GUI
import threading
from utils import ConfigManager


if __name__ == "__main__":
    # Initialize objects
    config_manager = ConfigManager()
    config_manager.load_config()
    server = get_server()
    gui = GUI()

    # Starting server in thread because app have two main loops
    server.gamestate.on_update(gui.on_update_gamestate)
    thread = threading.Thread(None, server.serve_forever)
    thread.start()

    # Starting GUI
    gui.mainloop()

    # Closing server and thread, save configuration to file
    server.shutdown()
    thread.join()
    config_manager.save_config()
