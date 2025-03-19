from pathlib import Path
from unittest import TestCase

from mvc.models.phonebook import Phonebook


class PhonebookTestCase(TestCase):

    def setUp(self) -> None:
        self.phonebook = Phonebook(filepath='tmp.json')

    def tearDown(self):
        Path(self.phonebook.filepath).unlink()
    
    def test_init_phonebook(self):
        self.phonebook.init_phonebook()
        self.assertTrue(isinstance(self.phonebook.load(), list))
    
    def test_save_load_phonebook(self):
        self.phonebook.save([('test', 'test', 'test')])
        self.assertTrue(self.phonebook.load())

        data = self.phonebook.load()
        self.assertEqual(data[0], ['test', 'test', 'test'])