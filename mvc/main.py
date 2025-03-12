from mvc.controllers.app_controller import PhonebookController
from mvc.models import Phonebook
from mvc.views.menu import Menu

def run_app():
    
    phonebook = Phonebook()
    phonebook.init_phonebook()
    
    
    controller = PhonebookController(phonebook)
    
    
    menu = Menu(controller)
    
    
    while True:
        menu.menu_show_main()

if __name__ == '__main__':
    run_app()