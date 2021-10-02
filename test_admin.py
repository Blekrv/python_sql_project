import unittest
import re
from admin import Admin, SuperAdmin
from connection import Connection
from validation import ORDERS, PRODUCT, Validate, USERS, CATEGORY, SUBCATEGORY, SELECT_TABLE

# valid data
VALID_EMAIL = 'vova@zel.com'
VALID_PASSWORD = 'iamPresident!'
# invalid data
INVALID_EMAIL = 'vova@@zel.com'
INVALID_PASSWORD = 12345678
# valid data
VALID_ADMIN_EMAIL = 'vova@zel.pre'
VALID_ADMIN_PASSWORD = 'iamPresident!'


ADMIN_DATA = [{
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
INVALID_ADMIN_DATA = [{
    "first_name": "Vladimir",
    "last_name": "Zelenskiy",
    "date_of_bitrth": "06.06.1978",
    "phone": "+380966809260",
    "address": "Streee1",
    "password": "q1w2e3r4!A",
    "email": "vova@mail.pre",
    "role": "admin",
    "discount": 'gg'
}]

CATEGORY_DATA = [{
    'category_name': "blouse"
}]

PRODUCT_DATA = [{
    "code": 34523,
    "product_name": 'tunic',
    "unit_price": 864.0,
    "count": 10,
    "description": 'red short tunic',
    "img": 'tunic-1.png',
    "sub_category_id": 4,
}]


class SuperAdminTests(unittest.TestCase):

    def setUp(self):
        # create SuperAdmin
        self.super_admin = SuperAdmin(VALID_EMAIL, VALID_PASSWORD)
        # return super().setUp()
        pass

    def tearDown(self):
        selector = Connection()._getNextId('users')-1
        # self.super_admin.delete_admin(selector)
        return super().tearDown()

    def clear_record(self, table):
        selector = Connection()._getNextId(table)-1
        self.super_admin.delete_admin(selector)

    def test_create_SuperAdmin(self):
        super_admin_val = SuperAdmin(VALID_EMAIL, VALID_PASSWORD)
        self.assertIsInstance(super_admin_val, SuperAdmin)
        print('Test 1.1: pass.')

    def test_create_invalid_SuperAdmin(self):
        super_admin_inv = SuperAdmin(INVALID_EMAIL, INVALID_PASSWORD)
        email_pattern = re.compile(
            r'^([a-zA-Z0-9-_\*\.]+)@([a-zA-Z0-9-]+)(\.[a-zA-Z0-9]+)+$')

        self.assertNotRegex(INVALID_EMAIL,
                            email_pattern, 'Incorrect email!')
        self.assertNotIsInstance(INVALID_PASSWORD, str,
                                 f'Incorect data type! It must been str but returned {type(INVALID_PASSWORD)}')
        self.assertIsInstance(super_admin_inv, SuperAdmin)
        print('Test 1.2: pass.')

    def test_add_admin(self):
        Validate().validate(ADMIN_DATA[0], USERS, 'users')
        response = self.super_admin.add_admin(ADMIN_DATA)
        self.assertEqual(response, 'Insert done!')
        print('Test 1.3: pass.')


class AdminTests(unittest.TestCase):

    def setUp(self):
        self.admin = Admin(VALID_ADMIN_EMAIL, VALID_ADMIN_PASSWORD)

    def tearDown(self):
        selector = Connection()._getNextId('users')-1
        selector = f"id = '{selector}'"
        return super().tearDown()

    def clear_record(self, table):
        selector = Connection()._getNextId(table)-1
        selector = f"id = '{selector}'"
        Connection()._deleteData(table, selector)

    def test_create_Admin(self):
        admin_val = Admin(VALID_ADMIN_EMAIL, VALID_ADMIN_PASSWORD)
        self.assertIsInstance(admin_val, Admin)
        print('Test 2.1: pass.')

    def test_create_invalid_Admin(self):
        admin_inv = Admin(INVALID_EMAIL, INVALID_PASSWORD)
        email_pattern = re.compile(
            r'^([a-zA-Z0-9-_\*\.]+)@([a-zA-Z0-9-]+)(\.[a-zA-Z0-9]+)+$')

        self.assertNotRegex(INVALID_EMAIL,
                            email_pattern, 'Incorrect email!')
        self.assertNotIsInstance(INVALID_PASSWORD, str,
                                 f'Incorect data type! It must been str but returned {type(INVALID_PASSWORD)}')
        self.assertIsInstance(admin_inv, Admin)
        print('Test 2.2: pass.')

    def test_add_pr_category(self):
        Validate().validate(CATEGORY_DATA[0], CATEGORY, 'product_category')
        response = self.admin.add_pr_category(CATEGORY_DATA)
        self.assertEqual(response, 'Insert done!')
        print('Test 2.3: pass.')
        self.clear_record('product_category')

    def test_edit_pr_category(self):
        Validate().validate(CATEGORY_DATA[0], CATEGORY, 'product_category')
        Validate().validate_table('product_category',
                                  SELECT_TABLE, "category_name = 'water'")
        edit = self.admin.edit_pr_category(
            CATEGORY_DATA[0], "category_name = 'water'")
        self.assertEqual(edit, 'Update done!')
        print('Test 2.4: pass.')

    def test_delete_pr_category(self):
        Validate().validate_table('product_category',
                                  SELECT_TABLE, "category_name = 'wardrobe'")
        dele = self.admin.delete_pr_category('wardrobe')
        self.assertEqual(dele, 'Item was deleted!')
        print('Test 2.5: pass.')

    def test_get_order_info(self):
        Validate().validate_table('orders',
                                  SELECT_TABLE, "date_of_order")
        Validate().validate({'date_of_order': '02-10-2021'}, ORDERS, 'orders')
        info = self.admin.get_order_info(
            category='date_of_order', selector='02-10-2021')
        self.assertTrue(info, 'Is not data!')
        print('Test 2.6: pass.')

    def test_get_order_info_none(self):
        Validate().validate_table('orders',
                                  SELECT_TABLE, "date_of_order")
        Validate().validate({'date_of_order': '03-10-2021'}, ORDERS, 'orders')
        info = self.admin.get_order_info(
            category='date_of_order', selector='03-10-2021')
        self.assertFalse(info, 'The data is there!')
        print('Test 2.7: pass.')

    def test_add_product(self):
        Validate().validate(PRODUCT_DATA[0], PRODUCT, 'product')

        response = self.admin.add_product(PRODUCT_DATA)
        self.assertEqual(response, 'Insert done!')
        print('Test 2.8: pass.')
        self.clear_record('product')


if __name__ == '__main__':
    unittest.main()
