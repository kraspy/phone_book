from mvc.models import Phonebook
from mvc.models import Menu

def run_app():
    phonebook = Phonebook()
    phonebook.init_phonebook()

    menu = Menu(phonebook=phonebook)

    while True:
        menu.menu_show_main()
