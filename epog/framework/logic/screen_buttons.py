from framework.logic.blessings import get_blessing_objects
from framework.logic.idols import get_idols
from framework.logic.main_menu import main_menu

screen_buttons = {
    'MainMenu': main_menu
}

button_objects = {
    'Blessing': get_blessing_objects,
    'Idols': get_idols
}
