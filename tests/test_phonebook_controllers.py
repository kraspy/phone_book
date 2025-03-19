from pathlib import Path
from unittest import TestCase

from mvc.common.errors import ContactError
from mvc.controllers.app_controller import Phonebook, PhonebookController


class PhonebookControllerTestCase(TestCase):
    def setUp(self):
        self.phonebook = Phonebook(filepath='tmp.json')
        self.phonebook.init_phonebook()
        self.controller = PhonebookController(self.phonebook)

    def tearDown(self):
        Path(self.phonebook.filepath).unlink()

    def test_create_contact(self):
        user_with_correct_data = ['user name', '123456789', 'comment']
        user_with_non_digit_phone_number = ['user name 2', 'asd', 'comment']
        user_with_short_phone_number = ['user name 3', '12345678', '']
        user_with_long_phone_number = ['user name 4', '1234567891011', '']


        self.controller.create_contact(*user_with_correct_data)
        self.assertEqual(self.phonebook.load(), [user_with_correct_data])

        self.assertRaises(ContactError, self.controller.create_contact, *user_with_non_digit_phone_number)
        self.assertRaises(ContactError, self.controller.create_contact, *user_with_short_phone_number)
        self.assertRaises(ContactError, self.controller.create_contact, *user_with_long_phone_number)
    
    def test_search_contact(self):
        contacts = [
            ['user name 1', '123123123', 'comment 1'],
            ['user name 2', '456456456456', 'comment 2'],
            ['user name 3', '789789789789', 'comment 3'],
            ['user name 4', '9998887766', 'comment 4'],
            ['user name 5', '111222333', 'comment 5'],
            ['user name 6', '444555666', 'comment 6'],
        ]

        self.phonebook.save(contacts)

        cases = [
            ('user', contacts),
            ('444', [contacts[5]]),
            ('7', [contacts[2], contacts[3]]),
            ('comment 2', [contacts[1]]),
        ]

        for query, expected in cases:
            with self.subTest(msg=f'Поиск по "{query}"'):
                self.assertEqual(self.controller.find_contacts(query), expected)
    
    def test_update_contact(self):
        contacts = [
            ['user name 1', '111111111', 'comment 1'],
            ['user name 2', '222222222', 'comment 2'],
            ['user name 3', '333333333', 'comment 3'],
        ]

        self.phonebook.save(contacts)
        self.controller.update_contact(0, 'name', 'new name')
        self.assertEqual(self.controller.get_all_contacts()[0][0], 'new name')
        self.controller.update_contact(1, 'phone', '444444444')
        self.assertEqual(self.controller.get_all_contacts()[1][1], '444444444')
        self.controller.update_contact(2, 'comment', 'new comment')
        self.assertEqual(self.controller.get_all_contacts()[2][2], 'new comment')

    def test_delete_contact(self):
        contacts = [
            ['user name 1', '111111111', 'comment 1'],
            ['user name 2', '222222222', 'comment 2'],
            ['user name 3', '333333333', 'comment 3'],
        ]

        self.phonebook.save(contacts)

        self.assertRaises(ContactError, self.controller.delete_contact, 3)
        self.controller.delete_contact(0)
        self.assertEqual(self.controller.get_all_contacts(), contacts[1:])
        self.controller.delete_contact(1)
        self.assertEqual(self.controller.get_all_contacts(), contacts[1:2])
        self.controller.delete_contact(0)
        self.assertEqual(self.controller.get_all_contacts(), [])