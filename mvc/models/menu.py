import sys

import click
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from pydantic import ValidationError

from mvc.errors import ContactError
from mvc.models import Phonebook, Contact
from mvc.utils import menu_decorator


class Menu:
    def __init__(self, phonebook: Phonebook, width: int = 40):
        self.menu_items = [
            ('Показать контакты', self.menu_show_contacts),
            ('Создать новый контакт', self.menu_create_contact),
            ('Найти контакт', self.menu_find_contact),
            ('Изменить контакт', self.menu_change_contact),
            ('Удалить контакт', self.menu_delete_contact),
            ('Выйти', self.menu_close_app),
        ]
        self.width = width
        self.phonebook = phonebook

    def go_to_menu():
        print('---')
        input('Нажмите Enter, что бы вернуться в меню.')
        click.clear()

    @menu_decorator
    def menu_show_main(self) -> None:
        click.echo('{: ^40}'.format('Меню'))
        click.echo('=' * self.width)

        menu_items = [f'{i}: {item[0]}' for i, item in enumerate(self.menu_items)]

        print('\n'.join(menu_items))
        print('---')

        user_input = Prompt.ask('Выберите пункт меню')

        if not user_input.isdigit():
            return

        menu_index = int(user_input)

        if not 0 <= int(menu_index) < len(self.menu_items):
            return

        self.menu_items[int(menu_index)][1]()

    @menu_decorator
    def menu_show_contacts(self) -> None:
        contacts = self.phonebook.load()

        table = Table(title='Список контактов')
        table.add_column('Наименование')
        table.add_column('Телефон')
        table.add_column('Комментарий')

        if contacts:
            for contact in contacts:
                table.add_row(*contact)
            print(table)
        else:
            print('Нет контактов!')

    @menu_decorator
    def menu_create_contact(self) -> None:
        contacts: list[tuple[str, str, str]] = self.phonebook.load()

        click.echo('{: ^40}'.format('Новый контакт'))
        click.echo('=' * self.width)

        try:
            new_contact = Contact(
                name=input('Наименование (обязательно): '),
                phone=input('Номер телефона (9-12 цифр): '),
                comment=input('Коммент (не обязательно): '),
            )
        except ContactError as e:
            print(f'[red]{e}[/red]')
            return



        contacts.append(new_contact.model_dump_tuple())
        self.phonebook.save(contacts)

        print('[green]Контакт успешно создан![/green]')

    @menu_decorator
    def menu_find_contact(self) -> None:
        click.echo('{: ^40}'.format('Поиск'))
        click.echo('=' * self.width)

        req = input('Введите строку поиска: ')

        contacts = self.phonebook.load()
        found_contacts = []

        if contacts:
            for contact in contacts:
                for item in contact:
                    if req.lower() in item.lower():
                        found_contacts.append(contact)
                        break
            if found_contacts:
                click.clear()
                print('[green]Найденные контакты:[/green]')

                table = Table()
                table.add_column('Наименование')
                table.add_column('Телефон')
                table.add_column('Комментарий')

                for contact in found_contacts:
                    table.add_row(*contact)
                print(table)

            else:
                print('[red]Совпадений нет.[/red]')

        else:
            print('[red]Контактов нет.[/red] Искать нечего.')

    @menu_decorator
    def menu_change_contact(self) -> None:
        contacts = self.phonebook.load()

        if not contacts:
            print('[red]Контактов нет. Изменять нечего.[/red]')
            return

        table = Table(title='Список контактов')
        table.add_column('№')
        table.add_column('Наименование')
        table.add_column('Телефон')
        table.add_column('Комментарий')

        for i, contact in enumerate(contacts):
            table.add_row(str(i), *contact)

        print(table)

        contact_number = input('Введите номер контакта, который необходимо изменить: ')

        if not (contact_number.isdigit() and 0 <= int(contact_number) < len(contacts)):
            print('[red]НЕкорректный номер контакта.[/red]')
            return

        contact_index = int(contact_number)

        name, phone, comment = contacts[contact_index]


        print(
            f'\n[bold]Текущий контакт:[/bold]\nИмя: {name}\nТелефон: {phone}\nКомментарий: {comment}'
        )

        change_number = input(
            '\nВыберите, что нужно изменить (0 - Имя, 1 - Телефон, 2 - Комментарий): '
        )

        if not (change_number.isdigit() and int(change_number) in {0, 1, 2}):
            print('[red]НЕкорректный номер поля для изменения![/red]')
            return

        index_texts = [
            'Введите новое имя: ',
            'Введите новый телефон (9-12 цифр): ',
            'Введите новый комментарий: ',
        ]

        change_index = int(change_number)
        new_value = input(index_texts[change_index])

        try:
            Contact.validate_name(new_value) if change_index == 0 else Contact.validate_phone(new_value)
        except ContactError as e:
            print(f'[red]{e}[/red]')
            return

        match change_index:
            case 0:
                contacts[contact_index] = Contact(new_value, phone, comment)
            case 1:
                contacts[contact_index] = Contact(name, new_value, comment)
            case 2:
                contacts[contact_index] = Contact(name, phone, new_value)

        self.phonebook.save(contacts)
        print('[green]Контакт успешно изменен![/green]')

    @menu_decorator
    def menu_delete_contact(self) -> None:
        contacts = self.phonebook.load()

        if not contacts:
            print('[red]Контактов нет. Удалять нечего.[/red]')
            return

        table = Table(title='Контакты')
        table.add_column('№')
        table.add_column('Наименование')
        table.add_column('Телефон')
        table.add_column('Комментарий')

        for i, contact in enumerate(contacts):
            table.add_row(str(i), *contact)

        print(table)

        selected_index = input('Введите номер контакта, который необходимо удалить: ')

        if selected_index.isdigit() and 0 <= int(selected_index) < len(contacts):
            selected_index = int(selected_index)
            removed_contact = contacts.pop(selected_index)
            self.phonebook.save(contacts)
            print(f'[green]Контакт "{removed_contact[0]}" успешно удален![/green]')
        else:
            print('[red]Ошибка! Введите корректный номер контакта.[/red]')

    @staticmethod
    def menu_close_app() -> None:
        sys.exit(0)
