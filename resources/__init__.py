import json
import os

verbose = False

basic_sample_size = 5
days_to_keep_around = 4


desktop_path = "C:\\Users\\Petr\\Desktop"
icons_path = "C:\Program Files (x86)\Steam\steam\games"

game_name_to_id = {'skyrim':72850,}
game_id_to_name = {
    72850: 'Skyrim',
    509250: "To The Top"}
icon_map = {72850:"C:\Program Files (x86)\Steam\steam\games\e15fa6de9b0120058a1876db6c3a22ccc6dac9d5.ico"}

def get_games_list():
    with open('./FullGamesList.txt', 'r') as f:
        return json.load(f)



# for hardcode
lib_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
games_shortcuts_folder = os.path.join(lib_root, 'resources', 'GamesShortcuts')
app_data_path = os.path.join(lib_root, 'resources', 'app_data.json')
app_data = dict(current_shortcuts = [])

shortcut_placeholder_path = os.path.join(lib_root, 'resources', 'ShortcutPlaceholder')

#constants
# desktop
# map_game_id_to_name = {
# }
# games_names = map_game_id_to_name.values()
