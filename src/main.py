from gui import MakeoverStudioGui
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    studio = MakeoverStudioGui(root)
    studio.run()
