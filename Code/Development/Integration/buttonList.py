import tkinter as tk
from tkinter import *
from tkinter.ttk import *

class ButtonList():
    def __init__(self, controller):
        self.buttons = []

    def make_button(self, frame, name):
        button = tk.Button(frame, text=name)
        self.buttons.append(button)

    def config_button(self, index, command):
        self.buttons[index].config(command=command)

    def show_button(self, position, index):
        self.buttons[index].pack(side=position, fill=X, expand=1)

    # def get_index(self, button):
    #   return self.buttons.index(button)
