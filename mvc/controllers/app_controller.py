from mvc.models import Phonebook, Contact
from mvc.common.errors import ContactError

class PhonebookController:
    def __init__(self, phonebook: Phonebook) -> None:
        self.phonebook = phonebook

    def get_all_contacts(self) -> list[tuple[str, str, str]]:
        return self.phonebook.load()

    def create_contact(self, name: str, phone: str, comment: str) -> None:
        contacts = self.phonebook.load()
        new_contact = Contact(name=name, phone=phone, comment=comment)
        contacts.append(new_contact.to_tuple())
        self.phonebook.save(contacts)

    def update_contact(self, index: int, field: str, value: str) -> None:
        contacts = self.phonebook.load()
        if not (0 <= index < len(contacts)):
            raise ContactError("Некорректный индекс контакта")
            
        name, phone, comment = contacts[index]
        match field:
            case "name":
                Contact.validate_name(value)
                name = value
            case "phone":
                Contact.validate_phone(value)
                phone = value
            case "comment":
                comment = value
                
        contacts[index] = Contact(name, phone, comment).to_tuple()
        self.phonebook.save(contacts)

    def delete_contact(self, index: int) -> tuple[str, str, str]:
        contacts = self.phonebook.load()
        if not (0 <= index < len(contacts)):
            raise ContactError("Некорректный индекс контакта")
        removed_contact = contacts.pop(index)
        self.phonebook.save(contacts)
        return removed_contact

    def find_contacts(self, query: str) -> list[tuple[str, str, str]]:
        contacts = self.phonebook.load()
        return [
            contact for contact in contacts 
            if any(query.lower() in field.lower() for field in contact)
        ]

def run_app():
    phonebook = Phonebook()
    phonebook.init_phonebook()
    
    controller = PhonebookController(phonebook)  
    menu = Menu(controller=controller)  

    while True:
        menu.menu_show_main()
