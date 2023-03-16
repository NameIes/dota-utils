import tkinter as tk
from abc import abstractmethod


class BaseHook(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(bg='#2C313A', *args, **kwargs)
        self.grid_propagate(False)

    @abstractmethod
    def on_update(self, gamestate):
        pass
