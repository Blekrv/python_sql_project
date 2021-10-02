import re
import unittest
# REdEX paterns

name_pattern = r'^([a-zA-Zа-щА-ЩЬьЮюЯяЇїІіЄєҐґ]+)\-?([a-zA-Zа-щА-ЩЬьЮюЯяЇїІіЄєҐґ]+)$'
email_pattern = r'^([a-zA-Z0-9-_\*\.]+)@([a-zA-Z0-9-]+)(\.[a-zA-Z0-9]+)+$'
password_pattern = r'^((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,}))|((?=.*[a-z])(?=.*[A-Z])(?=.*[^A-Za-z0-9])(?=.{8,}))$'
phone_pattern = r'^\+\d{12}$'
date_pattern = r'^([0-3]?[0-9])(\.|\-|\/)([0-1]?[0-9])(\.|\-|\/)(\d{4})$'
address_pattern = r"^[A-Za-z0-9'\.\-\s\,]{10,}$"
product_pattern = r"^[A-Za-z0-9'\.\-\s]{2,}$"
role_pattern = r'^(admin|customer|superAdmin)$'
number_pattern = r'^\d+\.?[0-9]*$'
img_pattern = r'^([A-Za-z0-9\_\-\.\S])+[\.](jpg|png|jpeg)$'

# models
USERS = {
    "id": [int, number_pattern],
    "first_name": [str, name_pattern],
    "last_name": [str, name_pattern],
    "date_of_bitrth": [str, date_pattern],
    "phone": [str, phone_pattern],
    "address": [str, address_pattern],
    "password": [str, password_pattern],
    "email": [str, email_pattern],
    "role": [str, role_pattern],
    "discount": [int, number_pattern]
}
ORDERS = {
    "id": [int, number_pattern],
    "date_of_order": [str, date_pattern],
    "customer_id": [int, number_pattern],
    "product_id": [int, number_pattern],
    "price": [float, number_pattern],
    "count": [int, number_pattern],
    "discount": [int, number_pattern],
    "total": [float, number_pattern],
}
PRODUCT = {
    "id": [int, number_pattern],
    "code": [int, number_pattern],
    "product_name": [str, product_pattern],
    "unit_price": [float, number_pattern],
    "count": [int, number_pattern],
    "description": [str, address_pattern],
    "img": [str, img_pattern],
    "sub_category_id": [int, number_pattern],
}
SUBCATEGORY = {
    "id": [int, number_pattern],
    "sub_category_name": [str, product_pattern],
    "category_id": [int, number_pattern],
}
CATEGORY = {
    "id": [int, number_pattern],
    "category_name": [str, product_pattern],

}
SELECT_TABLE = {
    'users': USERS,
    'orders': ORDERS,
    'product': PRODUCT,
    'product_subcategory': SUBCATEGORY,
    'product_category': CATEGORY,
}


class Validate(unittest.TestCase):
    def validate(self, request, model, model_name):
        for key in request:
            self.assertIn(key, model,
                          f'Field "{key}" is not in {model_name} model. Incorrect field name!')
            self.assertIsInstance(request[key], model[key][0],
                                  f'Field "{key}" has invalid data type for {model_name} model, it must been {model[key][0].__name__}. Type error!')
            value = request[key].strip() if isinstance(
                request[key], str) else str(request[key])
            self.assertRegex(value, model[key][1],
                             f'Field "{key}" has incorrect value for {model_name} model. Value error!')

    def validate_table(self, table, model, column_table):

        column = [item for key in model for item in model[key]]
        first_word = re.findall(r'\w+', column_table)[0]

        self.assertIn(table, model.keys(
        ),  f'Field "{table}" is not in {model.keys()} model. Incorrect field name!')
        self.assertIn(first_word, column,
                      f'Field "{first_word}" is not in {table} model. Incorrect field name!')


if __name__ == '__main__':
    admin_1_data = [{
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

    orders_data = [{
        "date_of_order": '2-5-2020',
        "customer_id": 1,
        "product_id": 2,
        "price": 1321.0,
        "count": 3,
        "discount": 0,
        "total": 3963.0,
    }]

    product_data = [{
        "code": 34523,
        "product_name": 'tunic',
        "unit_price": 864.0,
        "count": 10,
        "description": 'red short tunic',
        "img": 'tunic-1.png',
        "sub_category_id": 4,
    }]
    subcategory_data = [{
        "sub_category_name": 'tunic',
        "category_id": 3,
    }]
    category_data = [{
        "category_name": 'blouse',
    }]
