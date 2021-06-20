'''
# Retroarch Playlist Maker

## Source for .dat files:
https://github.com/libretro/libretro-database/tree/master/metadat/fbneo-split
https://github.com/libretro/libretro-database/tree/master/metadat/mame-split

## Information on how playlists work in Retroarch:
https://docs.libretro.com/guides/roms-playlists-thumbnails/
'''
import os
import json


class Playlist:

    playlists = []

    def __init__(self, name: str, source: str, output: str, filters=[], core='', search_recursively=False, rpi=False):
        '''Class that defines a playlist.

        Args:
            name (str): Name of the playlist following libretro's standard: https://github.com/libretro/libretro-database
            source (str): Path to folder containing ROMs.
            output (str): Path to '/retroarch/playlists'.
            filters (list, optional): Allowed file extentions without comma. Defaults to [].
            core (str, optional): Name of the core to be utilized. Defaults to 'DETECT'.
            search_recursively (bool): If True, scanner walks through subdirs recursively.
            rpi (bool, optional): True if running the script inside Lakka/Retropie, will change relative paths.
        '''
        self.name = name
        self.source = source
        self.output = output
        self.filters = filters
        self.core = core
        self.search_recursively = search_recursively
        self.files = self.scan_files()
        self.rpi = rpi
        Playlist.playlists.append(self)

    def scan_files(self) -> list:
        files = []
        try:
            if self.search_recursively:
                for root, _dirs, _files in os.walk(self.source):
                    for file_name in _files:
                        rel_dir = os.path.relpath(root, self.source)
                        rel_file = os.path.join(rel_dir, file_name)
                        if rel_file.startswith('.'):
                            rel_file = rel_file[2:]
                        files.append(rel_file)
            else:
                # Listing only files within a directory:
                files = [f for f in os.listdir(self.source) if os.path.isfile(os.path.join(self.source, f))]
            if not files:
                print(f'No files found: "{self.source}".')
        except FileNotFoundError:
            print(f'Directory not found: "{self.source}".')
        finally:
            return files

    def create_playlist(self):
        playlist = {
            'version': '1.4',
            'default_core_path': self.core,
            'default_core_name': '',
            'label_display_mode': 0,
            'right_thumbnail_mode': 0,
            'left_thumbnail_mode': 0,
            'sort_mode': 0,
            'items': []
            }

        if self.rpi:
            self.source = '/storage/roms/' + self.source
            self.output = '//LAKKA/Playlists'

        files = self.iterate_items()

        if self.rpi:
            for file in files:
                file['path'] = file['path'].replace('\\', '/')  # windows to unix

        playlist['items'] = files
        print(f'[{len(files)}] {self.name}')
        self.write_to_disk(playlist)

    def iterate_items(self) -> list:
        files = []
        for file in self.files:
            # If we have filters, and current file is not within it... ignore it!
            if self.filters and file.split('.')[-1] not in self.filters:
                pass
            # else, no filters OR the file is within the filters:
            else:
                name = os.path.split(file)[-1]
                name = name[:name.rfind('.')]
                item = {
                    'path': os.path.join(self.source, file),
                        'label': name,
                        'core_path': 'DETECT',
                        'core_name': 'DETECT',
                        'crc32': 'DETECT',
                        'db_name': self.name + '.lpl'
                    }
                files.append(item)

        return files

    def write_to_disk(self, playlist):
        file = os.path.join(self.output, self.name + '.lpl')

        with open(file, 'w') as f:
            json.dump(playlist, f, indent=4)


class Arcade(Playlist):

    def __init__(self, *args, dat_file='MAME 0.233 - Split.dat'):
        '''Class that defines an Arcade playlist.

        Args:
            *args: Inherited parameters from Playlist.
            dat_file (str, optional): path to dat file. Defaults to 'MAME 0.233 - Split.dat'.
        '''
        super().__init__(*args)
        self.dat_file = dat_file

    def iterate_items(self):
        files_found = []
        files = []
        bios = ['neogeo.zip']
        dat = open(self.dat_file, 'r')
        lines = dat.readlines()
        i = 0

        for line in lines:
            if line.startswith('	rom'):
                file = line.split()[3]
                if file in self.files and file not in bios:
                    files_found.append(file)
                    description = lines[i-3]
                    description = description[7:-2]
                    # description fix for '&'
                    # if any([i for i in ['_', '&amp;'] if i in description]): # unnecessary
                    if '_' in description:
                        description = description.replace('_', '&')
                    if '&amp;' in description:
                        description = description.replace('&amp;', '&')

                    item = {
                        'path': os.path.join(self.source, file),
                        'label': description,
                        'core_path': 'DETECT',
                        'core_name': 'DETECT',
                        'crc32': 'DETECT',
                        'db_name': self.name + '.lpl'
                        }

                    files.append(item)
            i += 1

        dat.close()

        missing_files = list(filter(lambda x: x not in files_found, self.files))
        if missing_files:
            print(f'[-{len(missing_files)}] {self.name} | Not found in .dat: {missing_files}')

        return files


def create_everything():
    for item in Playlist.playlists:
        item.create_playlist()
    input('\n[Done] Playlist(s) sucessfully created or updated.\n Press [ENTER] to exit.')
    
def change_mode():
    for item in Playlist.playlists:
        item.rpi = True
    print('[INFO] Lakka mode activated.\n')

def list_files(startpath='//LAKKA/ROMs'):
    text_file = open('ROMs list.txt', 'w')

    for root, _dirs, files in sorted(os.walk(startpath)):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        text_file.write('{}{}/\n'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in sorted(files):
            text_file.write('{}{}\n'.format(subindent, f))

    text_file.close()

# Entry examples
RETROARCH_PLAYLIST_PATH = r'C:\Users\Andreas\Desktop\RetroArch\playlists'


Arcade('FBNeo - Arcade Games', r'G:\Games\_Lakka\Arcade - Final Burn Alpha', RETROARCH_PLAYLIST_PATH, dat_file='FBNeo - Arcade Games.dat')
Arcade('MAME', r'G:\Games\Arcade - MAME', RETROARCH_PLAYLIST_PATH)
Playlist('Atari - 2600', r'G:\Games\_Lakka\Atari - 2600', RETROARCH_PLAYLIST_PATH)
Playlist('Atari - 7800', r'G:\Games\_Lakka\Atari - 7800', RETROARCH_PLAYLIST_PATH)
Playlist('Atari - Lynx', r'G:\Games\_Lakka\Atari - Lynx', RETROARCH_PLAYLIST_PATH)
Playlist('Nintendo - Game Boy Advance', r'G:\Games\_Lakka\Nintendo - Game Boy Advance', RETROARCH_PLAYLIST_PATH)
Playlist('Nintendo - Game Boy Color', r'G:\Games\_Lakka\Nintendo - Game Boy Color', RETROARCH_PLAYLIST_PATH)
Playlist('Nintendo - Game Boy', r'G:\Games\_Lakka\Nintendo - Game Boy', RETROARCH_PLAYLIST_PATH)
Playlist('Nintendo - Nintendo 64', r'G:\Games\_Lakka\Nintendo - Nintendo 64', RETROARCH_PLAYLIST_PATH)
Playlist('Nintendo - Nintendo Entertainment System', r'G:\Games\_Lakka\Nintendo - Nintendo Entertainment System', RETROARCH_PLAYLIST_PATH)
Playlist('Nintendo - Super Nintendo Entertainment System', r'G:\Games\_Lakka\Nintendo - Super Nintendo Entertainment System', RETROARCH_PLAYLIST_PATH)
Playlist('Sega - 32X', r'G:\Games\_Lakka\Sega - 32X', RETROARCH_PLAYLIST_PATH)
Playlist('Sega - Game Gear', r'G:\Games\_Lakka\Sega - Game Gear', RETROARCH_PLAYLIST_PATH)
Playlist('Sega - Master System - Mark III', r'G:\Games\_Lakka\Sega - Master System - Mark III', RETROARCH_PLAYLIST_PATH)
Playlist('Sega - Mega Drive - Genesis', r'G:\Games\_Lakka\Sega - Mega Drive - Genesis', RETROARCH_PLAYLIST_PATH)
Playlist('Sega - Saturn', r'G:\Games\Sega - Saturn', RETROARCH_PLAYLIST_PATH, ['cue', 'iso'], search_recursively=True)
Playlist('Sega - SG-1000', r'G:\Games\_Lakka\Sega - SG-1000', RETROARCH_PLAYLIST_PATH)
Playlist('SNK - Neo Geo Pocket Color', r'G:\Games\_Lakka\SNK - Neo Geo Pocket Color', RETROARCH_PLAYLIST_PATH)
Playlist('Sony - PlayStation', r'G:\Games\Sony - PlayStation 1', RETROARCH_PLAYLIST_PATH, ['iso', 'cue'], search_recursively=True)


if __name__ == '__main__':
    # change_mode()
    create_everything()
