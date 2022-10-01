from framework.util.util import open_scraped_data, group_by_value
blessings_data = open_scraped_data('blessings/bases')

normal_blessings = [blessing for blessing in blessings_data if 'Grand ' not in blessing['blessing_name']]
empowered_blessings = [blessing for blessing in blessings_data if 'Grand ' in blessing['blessing_name']]

grouped_normal_blessings = group_by_value(normal_blessings, key=lambda x: x['timeline'])
grouped_empowered_blessings = group_by_value(empowered_blessings, key=lambda x: x['timeline'])

def get_blessing_objects(blessing_index):
    return grouped_empowered_blessings[blessing_index]