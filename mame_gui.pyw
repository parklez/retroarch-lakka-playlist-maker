import tkinter as tk
from tkinter import filedialog
import os
from create_playlists import Arcade


exe_path = os.path.split(os.path.abspath(__file__))[0]
path_to_retroarch = ''
path_to_mame_roms = ''


def browse_something():
    folder = filedialog.askdirectory()
    return folder

def browse_retroarch():
    global path_to_retroarch
    path_to_retroarch = browse_something()

def browse_mame():
    global path_to_mame_roms
    path_to_mame_roms = browse_something()
    
def create_files():
   Arcade('MAME', source=path_to_mame_roms, output=path_to_retroarch + '/playlists/').create_playlist()


main = tk.Tk()
main.title("MAME Maker")
main.geometry('250x150')
main.configure(background='grey23')
main.resizable(0, 0)


retroarch_info = tk.Label(main, text="CHOOSE THE PATH TO RETROARCH",
                          bg='grey23',
                          fg='white').pack()
retroarch_browse = tk.Button(main, text='...', command=browse_retroarch).pack()
mame_info = tk.Label(main, text="CHOOSE THE PATH TO MAME's ROMs",
                     bg='grey23',
                     fg='white').pack()
mame_browse = tk.Button(main, text='...', command=browse_mame).pack()
final_button = tk.Button(main, text='CREATE PLAYLIST', command=create_files).pack()

main.mainloop()
