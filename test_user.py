import unittest
import re
from user_methods import Unregistered, Registered
from connection import Connection
from validation import Validate, SELECT_TABLE

# valid data
VALID_EMAIL = 'vova@zel.com'
VALID_PASSWORD = 'iamPresident!'
# invalid data
INVALID_EMAIL = 'vova@@zel.com'
INVALID_PASSWORD = 12345678

USER_DATA = [{
    "first_name": "Vladimir",
    "last_name": "Zelenskiy",
    "date_of_bitrth": "06.06.1978",
    "phone": "+380966809260",
    "address": "Streee1",
    "password": "q1w2e3r4!A",
    "email": "vova@mail.pre",
    "role": "admin",
    "discount": "20"
}]


class UsersTests(unittest.TestCase):

    def setUp(self):
        # create SuperAdmin
        self.register = Registered(VALID_EMAIL, VALID_PASSWORD)
        self.unregister = Unregistered()
        # return super().setUp()

    def tearDown(self):
        selector = Connection()._getNextId('users')-1
        selector = f"id = '{selector}'"
        # Connection()._deleteData('users', selector)
        return super().tearDown()

    def clear_record(self, table):
        selector = Connection()._getNextId(table)-1
        selector = f"id = '{selector}'"
        Connection()._deleteData(table, selector)

    def test_create_users(self):
        users_val = Registered(VALID_EMAIL, VALID_PASSWORD)
        self.assertIsInstance(users_val, Registered)
        print('Test 1.1: pass.')

    def test_create_invalid_Users(self):
        users_inv = Registered(INVALID_EMAIL, INVALID_PASSWORD)
        email_pattern = re.compile(
            r'^([a-zA-Z0-9-_\*\.]+)@([a-zA-Z0-9-]+)(\.[a-zA-Z0-9]+)+$')

        self.assertNotRegex(INVALID_EMAIL,
                            email_pattern, 'Incorrect email!')
        self.assertNotIsInstance(INVALID_PASSWORD, str,
                                 f'Incorect data type! It must been str but returned {type(INVALID_PASSWORD)}')
        self.assertIsInstance(users_inv, Registered)
        print('Test 1.2: pass.')

    def test_add_add_customer(self):

        response = self.unregister.add_customer(USER_DATA)
        self.assertEqual(response, 'Insert done!')
        print('Test 1.3: pass.')
        # self.clear_record('users')

    def test_get_product_info(self):
        Validate().validate_table('product', SELECT_TABLE, "code")
        model = [SELECT_TABLE[key] for key in SELECT_TABLE if key == 'product']
        Validate().validate({'code': 34523}, model[0], 'product')
        info = self.unregister.get_product_info(
            category='code', selector=34523)
        self.assertTrue(info, 'Is not data!')
        print('Test 1.4: pass.')

    def test_get_product_info_none(self):

        Validate().validate_table('product', SELECT_TABLE, "code")
        model = [SELECT_TABLE[key] for key in SELECT_TABLE if key == 'product']
        Validate().validate({'code': 345234}, model[0], 'product')

        info = self.unregister.get_product_info(
            category='code', selector=34523)
        self.assertFalse(info, 'The data is there!')
        print('Test 1.5: pass.')


if __name__ == '__main__':
    unittest.main()
