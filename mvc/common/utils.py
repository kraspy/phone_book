import json
from functools import wraps

import click

# ========================================
# Вспомогательные функции
# ========================================
def menu_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        click.clear()
        print('')
        func(*args, **kwargs)
        if func.__name__ != 'menu_show_main':
            print('---')
            input('Нажмите Enter, что бы вернуться в меню.')
            click.clear()
        click.clear()

    return wrapper
