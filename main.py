import json
import pathlib
import sys
from functools import wraps

import click
from rich import print
from rich.prompt import Prompt
from rich.table import Table

# ========================================
# ПЕРЕМЕННЫЕ ПРИЛОЖЕНИЯ
# ========================================
PHONEBOOK_FILEPATH = pathlib.Path('phonebook.json')
PHONEBOOK_INIT_TEXT = '[]'
FORMAT_WIDTH = 40


# ========================================
# Вспомогательные функции
# ========================================
def load_contacts() -> list | None:
    with open(PHONEBOOK_FILEPATH, 'r', encoding='utf-8') as file:
        content = json.loads(file.read())

        if isinstance(content, list):
            contacts = [(name, phone, comment) for name, phone, comment in content]
            return contacts


def dump_contacts(contacts: list) -> None:
    with open(PHONEBOOK_FILEPATH, 'w', encoding='utf-8') as file:
        file.write(json.dumps(contacts, ensure_ascii=False))


def menu_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        click.clear()
        print('')
        func(*args, **kwargs)
        if func.__name__ != 'menu_show_main':
            go_to_menu()
        click.clear()

    return wrapper


# ========================================
# ПУНКТЫ МЕНЮ
# ========================================
def go_to_menu():
    print('---')
    input('Нажмите Enter, что бы вернуться в меню.')
    click.clear()


@menu_decorator
def menu_show_main() -> None:
    click.echo('{: ^40}'.format('Меню'))
    click.echo('=' * FORMAT_WIDTH)

    menu_items = [f'{i}: {item[0]}' for i, item in enumerate(MENU)]

    print('\n'.join(menu_items))
    print('---')

    user_input = Prompt.ask('Выберите пункт меню')

    if not user_input.isdigit():
        return

    menu_index = int(user_input)

    if not 0 <= int(menu_index) < len(MENU):
        return

    MENU[int(menu_index)][1]()


@menu_decorator
def menu_show_contacts() -> None:
    contacts = load_contacts()

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
def menu_create_contact() -> None:
    contacts = load_contacts()

    click.echo('{: ^40}'.format('Новый контакт'))
    click.echo('=' * FORMAT_WIDTH)
    
    while not (name := input('Наименование: ')):
        print('[red]Имя не должно быть пустым![/red]')
    
    phone = input('Номер телефона: ')
    comment = input('Коммент: ')

    contacts.append((name, phone, comment))
    dump_contacts(contacts)

    print('[green]Контакт успешно создан![/green]')


@menu_decorator
def menu_find_contact() -> None:
    click.echo('{: ^40}'.format('Поиск'))
    click.echo('=' * FORMAT_WIDTH)
    
    req = input('Введите строку поиска: ')

    contacts = load_contacts()
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
def menu_change_contact() -> None:
    contacts = load_contacts()
    
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
        f'\n[bold]Текущий контакт:[/bold]\nИмя: {name}\nТелефон: {phone}\nКомментарий: {comment}')
    
    change_number = input('\nВыберите, что нужно изменить (0 - Имя, 1 - Телефон, 2 - Комментарий): ')
    
    if not (change_number.isdigit() and int(change_number) in {0, 1, 2}):
        print('[red]НЕкорректный номер поля для изменения![/red]')
        return
    
    change_index = int(change_number)
    new_value = input('Введите новое значение: ')
    
    match change_index:
        case 0:
            contacts[contact_index] = (new_value, phone, comment)
        case 1:
            contacts[contact_index] = (name, new_value, comment)
        case 2:
            contacts[contact_index] = (name, phone, new_value)
    
    dump_contacts(contacts)
    print('[green]Контакт успешно изменен![/green]')


@menu_decorator
def menu_delete_contact() -> None:
    contacts = load_contacts()
    
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
        dump_contacts(contacts)
        print(f'[green]Контакт "{removed_contact[0]}" успешно удален![/green]')
    else:
        print('[red]Ошибка! Введите корректный номер контакта.[/red]')


def menu_close_app() -> None:
    sys.exit(0)


# ========================================
# МЕНЮ
# ========================================
MENU = [
    ('Показать контакты', menu_show_contacts),
    ('Создать новый контакт', menu_create_contact),
    ('Найти контакт', menu_find_contact),
    ('Изменить контакт', menu_change_contact),
    ('Удалить контакт', menu_delete_contact),
    ('Выйти', menu_close_app),
]


# ========================================
# CLI
# ========================================
@click.command()
def run_app():
    if not PHONEBOOK_FILEPATH.exists():
        PHONEBOOK_FILEPATH.touch()

        with open(PHONEBOOK_FILEPATH, 'w') as file:
            file.write(PHONEBOOK_INIT_TEXT)

        print('[green]Файл для хранения контактов успешно создан![/green]')

    while True:
        menu_show_main()


if __name__ == '__main__':
    run_app()
