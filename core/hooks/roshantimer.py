import tkinter as tk
from .basehook import BaseHook


class RoshanTimer(BaseHook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tk.Label(self, text='Rosh')