import string
import os
from resources import desktop_path
import resources
import shutil
import time

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


def get_shortcut_icon_location(shortcut_path):
    import pythoncom
    from win32com.shell import shell, shellcon
    if shortcut_path.endswith('.url'):
        type1 = shell.CLSID_InternetShortcut
    elif shortcut_path.endswith('.lnk'):
        type1 = shell.CLSID_ShellLink
    type2 = shell.IID_IShellLink # for icon
    shortcut = pythoncom.CoCreateInstance(
        type1,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        type2
    )
    persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Load(shortcut_path)
    return trim(shortcut.GetIconLocation()[0], s='file:///').replace('%20', ' ')


def get_shortcut_target_path(shortcut_path):
    import pythoncom
    from win32com.shell import shell, shellcon
    if shortcut_path.endswith('.url'):
        type1 = shell.CLSID_InternetShortcut
        type2 = shell.IID_IUniformResourceLocator
    elif shortcut_path.endswith('.lnk'):
        type1 = shell.CLSID_ShellLink
        type2 = shell.IID_IShellLink
    else:
        raise Exception("Unsupported shortcut type, should be .url or .lnk")
    shortcut = pythoncom.CoCreateInstance(
        type1,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        type2
    )
    persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Load(shortcut_path)
    if shortcut_path.endswith('.url'):
        return shortcut.GetURL()
    elif shortcut_path.endswith('.lnk'):
        return shortcut.GetPath(0)[0]


def set_shortcut_icon_location(shortcut_path, icon_location):
    import pythoncom
    from win32com.shell import shell, shellcon
    if shortcut_path.endswith('.url'):
        type1 = shell.CLSID_InternetShortcut
    elif shortcut_path.endswith('.lnk'):
        type1 = shell.CLSID_ShellLink
    type2 = shell.IID_IShellLink # for icon
    shortcut = pythoncom.CoCreateInstance(
        type1,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        type2
    )
    persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Load(shortcut_path)
    shortcut.SetIconLocation(icon_location, 0)
    persist_file.Save(shortcut_path, 0)


def set_shortcut_target_path(shortcut_path, target_path):
    import pythoncom
    from win32com.shell import shell, shellcon
    if shortcut_path.endswith('.url'):
        type1 = shell.CLSID_InternetShortcut
        type2 = shell.IID_IUniformResourceLocator
    elif shortcut_path.endswith('.lnk'):
        type1 = shell.CLSID_ShellLink
        type2 = shell.IID_IShellLink
    else:
        raise Exception("Unsupported shortcut type, should be .url or .lnk")
    shortcut = pythoncom.CoCreateInstance(
        type1,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        type2
    )
    persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Load(shortcut_path)
    if shortcut_path.endswith('.url'):
        shortcut.SetURL(target_path)
    elif shortcut_path.endswith('.lnk'):
        shortcut.SetPath(0)[0]
    persist_file.Save(shortcut_path, 0)


# def transform_game_shortcut(game, target_past=None):
#     """
#     :param game:
#     :param target_past:
#     :return: Transform previous game shortcut into the new one
#     So that the location on the desktop remains the same!
#     Ridiculous, but delays between name and icon change are necessary!
#     """
#     delay = 3
#     from resources import games_shortcuts_folder
#     source_path = os.path.join(games_shortcuts_folder, game)
#     target_path = os.path.join(desktop_path, game)
#     if target_past is None:
#         shutil.copy(source_path, target_path)
#         return
#     # if target_past.rsplit('.', 1)[-1] == target_path.rsplit('.', 1)[-1]:
#     #     # same file type .url or .lnk, simple case
#     #     set_shortcut_target_path(target_path, get_shortcut_target_path(source_path))
#     #     time.sleep(delay)  # this is ridiculous
#     #     set_shortcut_icon_location(target_path, get_shortcut_icon_location(source_path))
#     #     time.sleep(delay)  # Probably this is because of windows internal desktop refresh rate, but still...
#     # else:
#     # difficult case, have to recreate.
#     # ignore for now.
#     shutil.copy(source_path, target_past)
#     time.sleep(delay)  # oh, wait, with delay this works...
#     shutil.move(target_past, target_path)
#     time.sleep(delay)  # This is necessary, sleep(1) doesnt work


def create_game_shortcut(game, hardcode_mode, path=desktop_path):
    if hardcode_mode:
        from resources import games_shortcuts_folder
        source_path = os.path.join(games_shortcuts_folder, game)
        target_path = os.path.join(desktop_path, game)

        if not os.path.exists(source_path):
            raise Exception("No shortcut for game {} found in shortcuts folder: {}".format(game, games_shortcuts_folder))

        if os.path.exists(target_path):
            write(read(source_path), target_path, mode='a')
        # else:
        #     import shutil
        #     shutil.copy(source_path, target_path)

        # if source_path.rsplit('.')
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
    load_app_data()
    old_shortcuts = list(resources.app_data['current_shortcuts'])
    res = []
    for shortcut in old_shortcuts:
        # verify that old shortcuts are not removed
        if not os.path.exists(os.path.join(desktop_path, shortcut)):
            old_shortcuts.remove(shortcut)
            if resources.verbose:
                print('Shortcut "{}" not found'.format(shortcut))
        else:
            res.append(shortcut)
    old_shortcuts = res

    # 2) sample games
    today_games = sample_games(hardcode_mode=hardcode_mode)

    # 3) create new shortcuts
    games_to_process = []
    for game in today_games:
        if game in old_shortcuts:
            old_shortcuts.remove(game)
        else:
            games_to_process.append(game)

    import shutil
    for i, game in enumerate(games_to_process):
        if resources.verbose:
            print(game)
        from resources import games_shortcuts_folder
        source_path = os.path.join(games_shortcuts_folder, game)
        target_path = os.path.join(desktop_path, game)
        if len(old_shortcuts) <= i is None:
            shutil.copy(source_path, target_path)
        else:
            target_past = os.path.join(desktop_path, old_shortcuts[i])
            shutil.copy(source_path, target_past)
    delay = 3
    time.sleep(delay)  # oh, wait, with delay this works...
    for i, game in enumerate(games_to_process[:len(old_shortcuts)]):
        target_past = os.path.join(desktop_path, old_shortcuts[i])
        target_path = os.path.join(desktop_path, game)
        shutil.move(target_past, target_path)

    for i, game in list(enumerate(old_shortcuts))[len(games_to_process):]:
        # replace unused old shortcuts with placeholders
        shutil.move(os.path.join(desktop_path, game), os.path.join(desktop_path, "GamePlaceholder{num:02d}".format(num=i)))
        shutil.copy(resources.shortcut_placeholder_path, os.path.join(desktop_path, "GamePlaceholder{num:02d}".format(num=i)))

    resources.app_data['current_shortcuts'] = today_games
    save_app_data()
    return today_games


def parse_steam_ids_from_shortcuts(shortcuts, output_path=None):
    if os.path.isdir(shortcuts):
        path = shortcuts
        shortcuts = [os.path.join(path, sc) for sc in os.listdir(path)]
    res = []
    for shortcut in shortcuts:
        if not shortcut.endswith('.url'):
            continue
        with open(shortcut, 'r') as f:
            text = f.read()
        import re
        re_line = r"steam://rungameid/(\d*)"
        res += re.findall(re_line, text)
    if output_path is not None:
        dump_json(res, output_path)

    return res



