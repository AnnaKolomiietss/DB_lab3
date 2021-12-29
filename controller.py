
from psycopg2 import Error
import model
import view
import time


class Controller:
    def __init__(self):
        self.v = view.View()
        self.m = model.Model()

    def print(self, table_name):
        t_name = self.v.valid.check_table_name(table_name).upper()
        if t_name:
            if t_name == 'CATEGORY':
                self.v.print_category(self.m.print_category())
            elif t_name == 'CATEGORY_PILL':
                self.v.print_category_pill(self.m.print_category_pill())
            elif t_name == 'PILL':
                self.v.print_pill(self.m.print_pill())
            elif t_name == 'MANUFACTURER':
                self.v.print_manufacturer(self.m.print_manufacturer())

    def delete(self, table_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            k_val = self.v.valid.check_pk(value)
            count = 0
            if t_name == 'Category' and k_val:
                count = self.m.find_pk_category(k_val)
            elif t_name == 'Category_pill' and k_val:
                count = self.m.find_pk_category_pill(k_val)
            elif t_name == 'Pill' and k_val:
                count = self.m.find_pk_pill(k_val)
            elif t_name == 'Manufacturer' and k_val:
                count = self.m.find_pk_manufacture(k_val)

            if count:
                if t_name == 'Category' or t_name == 'Pill':
                    count_c_p = self.m.find_fk_category_pill(k_val, t_name)
                    if count_c_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            if t_name == 'Category':
                                self.m.delete_data_category(k_val)
                            elif t_name == 'Pill':
                                self.m.delete_data_pill(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)


                    # if t_name == 'Category':
                    #     count_c_p = self.m.find_fk_category_pill('Category_pill', 'category_id', value)
                    # if t_name == 'Pill':
                    #     count_c_p = self.m.find('Category_pill', 'pill_id', value)[0]
                    # if count_c_p:
                    #     self.v.cannot_delete()
                    # else:
                    #     try:
                    #         self.m.delete_data(table_name, key_name, k_val)

                elif t_name == 'Manufacturer':
                    count_p = self.m.find_fk_pill(k_val)
                    if count_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data_manufacturer(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data_category_pill(k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()

    def update_category_pill(self, key: str, pill_id: int, category_id: int):
        if self.v.valid.check_possible_keys('Category_pill', 'id', key):
            count_c_p = self.m.find_pk_category_pill(int(key))
            c_p_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('Pill', 'id', pill_id):
            count_p = self.m.find_fk_category_pill(int(pill_id), 'Pill')
            p_val = self.v.valid.check_pk(pill_id)
        if self.v.valid.check_possible_keys('Category', 'id', category_id):
            count_c = self.m.find_fk_category_pill(int(category_id), 'Category')
            c_val = self.v.valid.check_pk(category_id)

        try:
            self.m.update_data_category_pill(key, p_val, c_val)
        except (Exception, Error) as _ex:
            self.v.sql_error(_ex)

    def update_category(self, key: str, name: str, description: str):
        if self.v.valid.check_possible_keys('Category', 'id', key):
            count_c = self.m.find_pk_category(int(key))
            c_val = self.v.valid.check_pk(key, count_c)

        try:
            self.m.update_data_category(c_val, name, description)
        except (Exception, Error) as _ex:
            self.v.sql_error(_ex)

    def update_pill(self, key: str, manufacturer_id: int, name: str, price: int):
        if self.v.valid.check_possible_keys('Pill', 'id', key):
            count_p = self.m.find_pk_pill(int(key))
            p_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('Manufacturer', 'id', manufacturer_id):
            count_m = self.m.find_fk_pill(int(manufacturer_id))
            m_val = self.v.valid.check_pk(manufacturer_id)

        try:
            self.m.update_data_pill(p_val, m_val, name, price)
        except (Exception, Error) as _ex:
            self.v.sql_error(_ex)

    def update_manufacturer(self, key: str, country: str, name: str, email: str):
        if self.v.valid.check_possible_keys('Manufacturer', 'id', key):
            count_m = self.m.find_pk_manufacture(int(key))
            m_val = self.v.valid.check_pk(key, count_m)

        try:
            self.m.update_data_manufacturer(m_val, country, name, email)
        except (Exception, Error) as _ex:
            self.v.sql_error(_ex)

    def insert_pill(self, key: str, manufacturer_id: int, name: str, price: int):
        if self.v.valid.check_possible_keys('Pill', 'id', key):
            count_p = self.m.find_pk_pill(int(key))
        if self.v.valid.check_possible_keys('Manufacturer', 'id', manufacturer_id):
            count_m = self.m.find_fk_pill(int(manufacturer_id))
            m_val = self.v.valid.check_pk(manufacturer_id)

        try:
            self.m.insert_data_pill(int(key), m_val, name, price)
        except (Exception, Error) as _ex:
            self.v.sql_error(_ex)

    def insert_category_pill(self, key: str, pill_id: int, category_id: int):
        if self.v.valid.check_possible_keys('Category_pill', 'id', key):
            count_c_p = self.m.find_pk_category_pill(int(key))
        if self.v.valid.check_possible_keys('Pill', 'id', pill_id):
            count_p = self.m.find_fk_category_pill(int(pill_id), 'Pill')
            p_val = self.v.valid.check_pk(pill_id)
        if self.v.valid.check_possible_keys('Category', 'id', category_id):
            count_c = self.m.find_fk_category_pill(int(category_id), 'Category')
            c_val = self.v.valid.check_pk(category_id)

        try:
            self.m.insert_data_category_pill(int(key), p_val, c_val)
        except (Exception, Error) as _ex:
            self.v.sql_error(_ex)

    def insert_category(self, key: str, name: str, description: str):
        if self.v.valid.check_possible_keys('Category', 'id', key):
            count_c = self.m.find_pk_category(int(key))
        try:
            self.m.insert_data_category(int(key), name, description)
        except (Exception, Error) as _ex:
            self.v.sql_error(_ex)

    def insert_manufacturer(self, key: str, name: str, country: str, email: str):
        if self.v.valid.check_possible_keys('Manufacturer', 'id', key):
            count_m = self.m.find_pk_manufacture(int(key))

        try:
            self.m.insert_data_manufacturer(int(key), name, country, email)
        except (Exception, Error) as _ex:
            self.v.sql_error(_ex)

    def generate(self, table_name: str, n: int):
        t_name = self.v.valid.check_table_name(table_name).upper()
        if t_name:
            if t_name == 'CATEGORY':
                self.m.category_data_generator(n)
            elif t_name == 'CATEGORY_PILL':
                self.m.category_pill_data_generator(n)
            elif t_name == 'PILL':
                self.m.pill_data_generator(n)
            elif t_name == 'MANUFACTURER':
                self.m.manufacturer_data_generator(n)

    def search_two(self):
        result = self.m.search_data_two_tables()
        self.v.print_search(result)

    def search_three(self):
        result = self.m.search_data_three_tables()
        self.v.print_search(result)

    def search_all(self):
        result = self.m.search_data_all_tables()
        self.v.print_search(result)

