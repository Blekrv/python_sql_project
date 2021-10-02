import psycopg2
from settings import *
from connection import Connection, _checkPassword, _checkEmail
import datetime
from validation import Validate, SELECT_TABLE


class SuperAdmin(Connection):

    def __init__(self, login: str, password: str):
        self.login = _checkEmail(login, 'superAdmin')
        self.password = _checkPassword(password, 'superAdmin')

    def login_self(self):
        return self._login_check(self.login, self.password)

    def add_admin(self, admin_data):
        if self.login_self():
            table = 'users'
            result = self._postData(table, admin_data)
        else:
            result = 'Incorrect login or password'
        return result

    def delete_admin(self, selector):
        if self.login_self():
            table = 'users'
            selector = f"id = '{selector}'"
            result = self._deleteData(table, selector)
        else:
            result = 'Incorrect login or password'
        return result


class Admin(Connection):

    def __init__(self, login, password):
        self.login = _checkEmail(login, 'Admin')
        self.password = _checkPassword(password, 'Admin')

    def login_self(self):
        return self._login_check(self.login, self.password)

    def add_pr_category(self, data):
        if self.login_self():
            table = 'product_category'
            result = self._postData(table, data)
        else:
            result = 'Incorrect login or password'
        return result

    def add_product(self, data):
        if self.login_self():
            table = 'product'
            result = self._postData(table, data)
        else:
            result = 'Incorrect login or password'
        return result

    def edit_pr_category(self, data, selector):
        if self.login_self():
            table = 'product_category'
            result = self._updateData(table, data, selector)
        else:
            result = 'Incorrect login or password'
        return result

    def delete_pr_category(self, selector):
        if self.login_self():
            table = 'product_category'
            selector = f"category_name = '{selector}'"
            result = self._deleteData(table, selector)
        else:
            result = 'Incorrect login or password'
        return result

    def get_order_info(self, category='', selector='',):

        model = [SELECT_TABLE[key] for key in SELECT_TABLE if key == 'orders']
        Validate().validate({category: selector}, model[0], 'orders')

        """
        category must be one of the item from the list:
        ['date_of_order', 'code']
        date format for selector: 2020-6-12
        """
        if self.login_self():
            categoryes = ['date_of_order', 'code']
            table = ('orders o',)

            fields = ("""o.id, o.date_of_order, concat(u.first_name,' ', u.last_name) as "customer",
                         p.product_name as "product_name", p.code as "product_id", o.price, o.count, o.discount, o.total""",)
            fieldNames = ["id", "date_of_order", "customer",
                          "product_name", "product_id", "price", "count", "discount", "total"]
            if category and category in categoryes and selector != '':
                if isinstance(selector, bool):
                    where = f"""where {category} = {selector}"""
                else:
                    where = f"""where {category} = '{selector}'"""
            else:
                where = ''
            selector = f""" left JOIN users u on u.id = o.customer_id
                            left JOIN product p on p.id = o.product_id 
                            {where}"""
            result = self._getData(table, fields, selector)
            changeRes = []
            for item in result:
                cort = {}
                for index, element in enumerate(item):
                    cort[fieldNames[index]] = element
                changeRes.append(cort)
        else:
            changeRes = 'Incorrect login or password'
        return changeRes


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

    admin_2 = Admin('Sania@mail.com', 'q1w2e3r4!A')

    rez = admin_2.get_order_info(
        category='date_of_order', selector='2021-09-2')
    print(rez)
    # --------------------------
    data = [{
        'category_name': "pants"
    }]
    add = admin_2.add_pr_category(data)
    print(add)
    # ------------------------
    data = {
        'category_name': "pants"
    }
    edit = admin_2.edit_pr_category(data, "category_name = 'hat'")
    print(edit)
    # --------------------------
    dele = admin_2.delete_pr_category('pants')
    print(dele)
    # --------------------------
