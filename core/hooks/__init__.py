from .camera import Camera
from .roshantimer import RoshanTimer


class HookManager:
    def __init__(self, hooks_parent) -> None:
        self.hooks = {
            'Camera': Camera(hooks_parent),
            'Roshan Timer': RoshanTimer(hooks_parent),
        }

    def get_hook_by_name(self, hook_name):
        return self.hooks[hook_name]

    def get_all_hook_names(self):
        return self.hooks.keys()

    def on_update(self, gamestate):
        for hook in self.hooks.values():
            hook.on_update(gamestate)
