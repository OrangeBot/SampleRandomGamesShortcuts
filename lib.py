import string
import os
from resources import desktop_path
import resources

from pyutils import *

def load_app_data(path=resources.app_data_path, update_resources=True):
    app_data = load_json(path)
    if update_resources:
        resources.app_data = app_data
    return app_data

def save_app_data(path=resources.app_data_path, app_data=None):
    if app_data is None:
        app_data = resources.app_data
    return dump_json(app_data, path)

def format_game_name(name):
    return ''.join([c for c in str(name) if c.lower() in string.ascii_lowercase])

def parse_game_id(game):
    game_name = format_game_name(game)
    from resources import game_name_to_id
    if game_name in game_name_to_id:
        return game_name_to_id[game_name]
    return game

def get_game_icon(game):
    # icon_path = "C:\Program Files (x86)\Steam\steam\games\dbf2331a2b54e4417f0e5611b52a5e7fa671f527.ico"
    # default

    game_id = parse_game_id(game)
    # map
    from resources import icon_map
    if game_id in icon_map:
        return icon_map[game_id]

    # random icon
    from resources import icons_path
    icons = [i for i in os.listdir(icons_path) if i.endswith('.ico') and os.path.join(icons_path, i) not in icon_map.values()]
    import random
    icon = random.choice(icons)
    return os.path.join(icons_path, icon)

def generate_game_name(game_id):
    from resources import game_id_to_name
    if game_id in game_id_to_name:
        return game_id_to_name[game_id]
    return "RandomGame_{game_id}".format(game_id=game_id)


def is_game_shortcut(filename, hardcode_mode):
    if hardcode_mode:
        from resources import games_shortcuts_folder
        return filename in os.listdir(games_shortcuts_folder)
    else:
        # from resources import get_games_list
        raise NotImplementedError
        # return trim(trim(filename, e='.lnk'), e='.url')


def sample_games(hardcode_mode):
    import random
    if hardcode_mode:
        from resources import games_shortcuts_folder
        games_list = [g for g in os.listdir(games_shortcuts_folder) if g.endswith('.lnk') or g.endswith('.url')]

        from resources import basic_sample_size
        return random.sample(games_list, basic_sample_size)
    else:
        raise NotImplementedError


def create_game_shortcut(game, hardcode_mode, path=desktop_path):
    if hardcode_mode:
        from resources import games_shortcuts_folder
        source_path = os.path.join(games_shortcuts_folder, game)
        target_path = os.path.join(desktop_path, game)

        if not os.path.exists(source_path):
            raise Exception("No shortcut for game {} found in shortcuts folder: {}".format(game, games_shortcuts_folder))

        import shutil
        shutil.copy(source_path, target_path)
    else:
        import pythoncom
        from win32com.shell import shell, shellcon

        game_id = parse_game_id(game)

        if game == game_id:
            name = generate_game_name(game_id)
        else:
            name = game

        url_text = "steam://rungameid/{game_id}".format(game_id=game_id)
        shortcut = pythoncom.CoCreateInstance(
            shell.CLSID_InternetShortcut,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IUniformResourceLocator
        )
        shortcut.SetURL(url_text)
        persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)

        shortcut_path = os.path.join(path, name + '.url')
        persist_file.Save(shortcut_path, 0)

        with open(shortcut_path, 'r+') as f:
            url_line = "URL={}\n".format(url_text)
            icon_path = get_game_icon(game_id)
            replacement_text = ["IconIndex=0\n", url_line, "IconFile={}\n".format(icon_path)]

            shortcut_text = f.read()
            key = "IDList="
            start = shortcut_text.find(key) + len(key)
            start += len(shortcut_text[:start].split('\n')) + 1
            f.seek(start)
            f.writelines(replacement_text)


def update_games_shortcuts(hardcode_mode=True):
    app_data = load_app_data()

    # 1) cleanup old shortcuts
    desktop_files = os.listdir(desktop_path)
    for filename in desktop_files:
        if is_game_shortcut(filename, hardcode_mode=hardcode_mode):
            if resources.verbose:
                print("Removing old shortcut {shortcut}".format(shortcut=filename))
            os.remove(os.path.join(desktop_path, filename))

    # 2) sample games
    today_games = sample_games(hardcode_mode=hardcode_mode)

    # 3) create new shortcuts
    for game in today_games:
        if resources.verbose:
            print(game)
        create_game_shortcut(game, hardcode_mode=hardcode_mode)

    return today_games


def parse_steam_ids(path):
    res = []
    for filename in os.listdir(path):
        if not filename.endswith('.url'):
            continue
        with open(os.path.join(path, filename), 'r') as f:
            text = f.read()
        import re
        re_line = r"steam://rungameid/(\d*)"
        res += re.findall(re_line, text)
    return res



