import sys
import click
from rich import print
from rich.prompt import Prompt
from rich.table import Table
from mvc.common.errors import ContactError
from mvc.common.utils import menu_decorator


class Menu:
    def __init__(self, controller: 'PhonebookController', width: int = 40):
        self.controller = controller
        self.width = width
        self.menu_items = [
            ('Показать контакты', self.menu_show_contacts),
            ('Создать новый контакт', self.menu_create_contact),
            ('Найти контакт', self.menu_find_contact),
            ('Изменить контакт', self.menu_change_contact),
            ('Удалить контакт', self.menu_delete_contact),
            ('Выйти', self.menu_close_app),
        ]

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
        contacts = self.controller.get_all_contacts()
        
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
        try:
            name = input('Наименование: ')
            phone = input('Номер телефона: ')
            comment = input('Комментарий: ')
            
            self.controller.create_contact(name, phone, comment)
            print('[green]Контакт успешно создан![/green]')
        except ContactError as e:
            print(f'[red]{e}[/red]')

    @menu_decorator
    def menu_find_contact(self) -> None:
        query = input('Введите строку поиска: ')
        found_contacts = self.controller.find_contacts(query)
        
        if not found_contacts:
            print('[red]Контакты не найдены[/red]')
            return
            
        table = Table(title='Найденные контакты')
        table.add_column('Наименование')
        table.add_column('Телефон')
        table.add_column('Комментарий')
        
        for contact in found_contacts:
            table.add_row(*contact)
        print(table)

    @menu_decorator
    def menu_change_contact(self) -> None:
        contacts = self.controller.get_all_contacts()

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
            print('[red]Некорректный номер контакта.[/red]')
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
            print('[red]Некорректный номер поля для изменения![/red]')
            return

        fields = ["name", "phone", "comment"]
        index_texts = [
            'Введите новое имя: ',
            'Введите новый телефон (9-12 цифр): ',
            'Введите новый комментарий: ',
        ]

        change_index = int(change_number)
        new_value = input(index_texts[change_index])

        try:
            self.controller.update_contact(
                contact_index, 
                fields[change_index], 
                new_value
            )
            print('[green]Контакт успешно изменен![/green]')
        except ContactError as e:
            print(f'[red]{e}[/red]')

    @menu_decorator
    def menu_delete_contact(self) -> None:
        contacts = self.controller.get_all_contacts()

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

        try:
            selected_index = int(selected_index)
            removed_contact = self.controller.delete_contact(selected_index)
            print(f'[green]Контакт "{removed_contact[0]}" успешно удален![/green]')
        except (ValueError, ContactError) as e:
            print('[red]Ошибка! Введите корректный номер контакта.[/red]')

    @staticmethod
    def menu_close_app() -> None:
        sys.exit(0)
