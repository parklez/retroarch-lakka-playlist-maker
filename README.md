# RetroArch/Lakka playlists in 1-click! 👾

RetroArch's built-in scanner *used to** be slow and skip some of my ROMs/ISOs.\
This script scans ROMs/Discs in given directory, and creates a playlist file which can be saved locally or over the network on a Lakka installation on a Raspberry Pi for example.

I originally made this to create playlists while on my main PC for my Raspberry Pi 2, running Lakka.\
*Since retroarch 1.8.2, there's now a manual scanner option built-in! [Read here](https://www.libretro.com/index.php/retroarch-1-8-2-released/)

## Requirements 🐍
- Python 3
- Some programming knowledge

## Download ⚡
- [Download this repository](https://github.com/parklez/retroarch-lakka-playlist-maker/archive/master.zip)
- Edit the end of `create_playlists.py` or import this as a module in your own python program.

Keep this project @ the same folder as your ROMs, that way you can double-click to update your playlists. 💡

<p align="center">
  <img src="https://raw.githubusercontent.com/parklez/retroarch-lakka-playlist-maker/master/img/explorer.png">
</p>

## Documentation 📝
For most cases use `Playlist` class:
```python
Playlist(name='System Name', # Must follow this: https://github.com/libretro/retroarch-assets/tree/master/xmb/automatic/png
         source='path/to/your/rom/',
         output='path/to/Retroarch/playlist/',
         filters=['cue', 'iso'], # Limits to specific file types, defaults to []
         core='path/to/core', # Defaults ''
         search_recuversively=False, # Scans for files within dirs
         rpi=False) # Changes output directory in case script is being run from another computer
```

For Arcade (MAME/FBNeo) games:
```python
Arcade(*args, # Same arguments as Playlist.
       dat_file='path/to/dat') # 'Mame 0.233 - Split.dat' or 'FBNeo - Arcade Games.dat' 
```

## Examples of use 🐕‍🦺
Open `create_playlists.py` and add a new line for each system/playlist you want to create following the examples given:

```python
RETROARCH_PLAYLIST_PATH = r'C:\Users\Andreas\Desktop\RetroArch\playlists'

Playlist('Nintendo - Super Nintendo Entertainment System', r'G:\Games\_Lakka\Nintendo - Super Nintendo Entertainment System', RETROARCH_PLAYLIST_PATH)
Arcade('MAME', r'G:\Games\Arcade - MAME', RETROARCH_PLAYLIST_PATH)
Arcade('FBNeo - Arcade Games', r'G:\Games\_Lakka\Arcade - Final Burn Alpha', RETROARCH_PLAYLIST_PATH, dat_file='FBNeo - Arcade Games.dat')
Playlist('Sony - PlayStation', r'G:\Games\Sony - PlayStation 1', RETROARCH_PLAYLIST_PATH, ['iso', 'cue'], search_recursively=True)
```