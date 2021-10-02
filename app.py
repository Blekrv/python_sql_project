from admin import Admin
from admin import SuperAdmin
from user_methods import Unregistered
from user_methods import Registered

from custom import respprint
# --------------------------------------------------------------------
admin_2 = Admin('vova@zel.com', 'iamPresident!')
# rez = admin_2.get_order_info(category='code', selector='202154')
rez = admin_2.get_order_info(category='code', selector='')
respprint(rez)
# print(rez)
# --------------------------------------------------------------------
customer_2 = Unregistered()

rez = customer_2.get_product_info(category='code', selector='454545')
respprint(rez)
# print(rez)
# --------------------------------------------------------------------
reg_customer_1 = Registered('vova@zel.pre', 'iamPresident!')
info = reg_customer_1.discount_card()
respprint(info)
# --------------------------------------------------------------------
