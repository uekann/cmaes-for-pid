import tkinter as tk
from tkinter import ttk

from .borad_cli import RiversiBoard, BitBoard
from .game_cli import GameEnv
from .enemy_cli import LearnedEnemy


class App(tk.Frame):
    
    def __init__(self, master):
        super().__init__(master=master)
        master.pack()