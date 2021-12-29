from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, select, and_
from sqlalchemy.orm import relationship
from db import Orders, Session, engine


def recreate_database():
    Orders.metadata.drop_all(engine)
    Orders.metadata.create_all(engine)


class Category(Orders):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, key, name, description):
        self.id = key
        self.name = name
        self.description = description

    def __repr__(self):
        return "{:>10}{:>35}{:>80}" \
            .format(self.id, self.name, self.description)

class Category_pill(Orders):
    __tablename__ = 'Category_pill'
    id = Column(Integer, primary_key=True)
    pill_id = Column(Integer, ForeignKey('Pill.id'))
    category_id = Column(Integer, ForeignKey('Category.id'))
    pills = relationship('Pill')
    categories = relationship('Category')
    def __init__(self, key, pill_id, category_id):
        self.id = key
        self.pill_id = pill_id
        self.category_id = category_id

    def __repr__(self):
        return "{:>10}{:>20}{:>20}" \
            .format(self.id, self.pill_id, self.category_id)


class Pill(Orders):
    __tablename__ = 'Pill'
    id = Column(Integer, primary_key=True)
    manufacturer_id = Column(Integer, ForeignKey('Manufacturer.id'))
    name = Column(String)
    price = Column(Integer)
    manufacturers = relationship('Manufacturer')

    def __init__(self, key, manufacturer_id, name, price):
        self.id = key
        self.manufacturer_id = manufacturer_id
        self.name = name
        self.price = price

    def __repr__(self):
        return "{:>10}{:>20}{:>25}{:>10}" \
            .format(self.id, self.manufacturer_id, self.name, self.price)


class Manufacturer(Orders):
    __tablename__ = 'Manufacturer'
    id = Column(Integer, primary_key=True)
    country = Column(String)
    name = Column(String)
    email = Column(String)

    def __init__(self, key, country, name, email):
        self.id = key
        self.country = country
        self.name = name
        self.email = email

    def __repr__(self):
        return "{:>10}{:>20}{:>20}{:>40}" \
            .format(self.id, self.country, self.name, self.email)

class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    def find_pk_category(self, key_value: int):
        return self.session.query(Category).filter_by(id=key_value).first()

    def find_pk_category_pill(self, key_value: int):
        return self.session.query(Category_pill).filter_by(id=key_value).first()

    def find_fk_category_pill(self, key_value: int, table_name: str):
        if table_name == "Pill":
            return self.session.query(Category_pill).filter_by(pill_id=key_value).first()
        elif table_name == "Category":
            return self.session.query(Category_pill).filter_by(category_id=key_value).first()

    def find_pk_pill(self, key_value: int):
        return self.session.query(Pill).filter_by(id=key_value).first()

    def find_fk_pill(self, key_value: int):
        return self.session.query(Pill).filter_by(manufacturer_id=key_value).first()

    def find_pk_manufacture(self, key_value: int):
        return self.session.query(Manufacturer).filter_by(id=key_value).first()

    def print_category(self):
        return self.session.query(Category).order_by(Category.id.asc()).all()

    def print_category_pill(self):
        return self.session.query(Category_pill).order_by(Category_pill.id.asc()).all()

    def print_pill(self):
        return self.session.query(Pill).order_by(Pill.id.asc()).all()

    def print_manufacturer(self):
        return self.session.query(Manufacturer).order_by(Manufacturer.id.asc()).all()

    def delete_data_category(self, key) -> None:
        self.session.query(Category).filter_by(id=key).delete()
        self.session.commit()

    def delete_data_category_pill(self, key) -> None:
        self.session.query(Category_pill).filter_by(id=key).delete()
        self.session.commit()

    def delete_data_pill(self, key) -> None:
        self.session.query(Pill).filter_by(id=key).delete()
        self.session.commit()

    def delete_data_manufacturer(self, key) -> None:
        self.session.query(Manufacturer).filter_by(id=key).delete()
        self.session.commit()

    def update_data_category(self, key: int, name: str, description: str) -> None:
        self.session.query(Category).filter_by(id=key) \
            .update({Category.name: name, Category.description: description})
        self.session.commit()

    def update_data_category_pill(self, key: int, pill_id: int, category_id: int) -> None:
        self.session.query(Category_pill).filter_by(id=key) \
            .update({Category_pill.pill_id: pill_id, Category_pill.category_id: category_id})
        self.session.commit()

    def update_data_pill(self, key: int, manufacturer_id: int, name: str, price: int) -> None:
        self.session.query(Pill).filter_by(id=key) \
            .update({Pill.manufacturer_id: manufacturer_id, Pill.name: name, Pill.price: price})
        self.session.commit()

    def update_data_manufacturer(self, key: int, county: str, name: str, email: str) -> None:
        self.session.query(Manufacturer).filter_by(id=key) \
            .update({Manufacturer.country: county, Manufacturer.name: name, Manufacturer.email: email})
        self.session.commit()

    def insert_data_category(self, key: int, name: str, description: str) -> None:
        category = Category(key=key, name=name, description=description)
        self.session.add(category)
        self.session.commit()

    def insert_data_category_pill(self, key: int, pill_id: int, category_id: int) -> None:
        category_pill = Category_pill(key=key, pill_id=pill_id, category_id=category_id)
        self.session.add(category_pill)
        self.session.commit()

    def insert_data_pill(self, key: int, manufacturer_id: int, name: str, price: int) -> None:
        pill = Pill(key=key, manufacturer_id=manufacturer_id, name=name, price=price)
        self.session.add(pill)
        self.session.commit()

    def insert_data_manufacturer(self, key: int, county: str, name: str, email: str) -> None:
        manufacturer = Manufacturer(key=key, country=county, name=name, email=email)
        self.session.add(manufacturer)
        self.session.commit()

    def category_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Category\""
                         "select (SELECT MAX(id)+1 FROM public.\"Category\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) \
                         FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''); ")

    def category_pill_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Category_pill\" "
                         "select (SELECT (MAX(id)+1) FROM public.\"Category_pill\"), "
                         "(SELECT id FROM public.\"Pill\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"Pill\")-1)))), "
                         "(SELECT id FROM public.\"Category\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"Category\")-1))));")

    def pill_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Pill\" select (SELECT MAX(id)+1 FROM public.\"Pill\"), "
                         "(SELECT id FROM public.\"Manufacturer\" LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.\"Manufacturer\")-1)))), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(15-5)+5):: integer)), ''), "
                         "FLOOR(RANDOM()*(100000-1)+1);")

    def manufacturer_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.\"Manufacturer\" select (SELECT MAX(id)+1 FROM public.\"Manufacturer\"), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-4)+4):: integer)), ''), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(25-10)+10):: integer)), '');")

    def search_data_two_tables(self):
        return self.session.query(Manufacturer) \
            .select_from(Pill) \
            .filter(and_(
            Manufacturer.country.ilike('Ukraine'),
            Pill.manufacturer_id <= 3,
            Pill.price <= 200
            ))\
            .all()

    def search_data_three_tables(self):
        return self.session.query(Manufacturer) \
            .select_from(Pill, Category_pill) \
            .filter(and_(
            Manufacturer.name.ilike('reckitt'),
            Pill.price <= 400,
            Category_pill.pill_id <= 9,
            ))\
            .all()

    def search_data_all_tables(self):
        return self.session.query(Manufacturer) \
            .select_from(Category_pill, Pill, Category) \
            .filter(and_(
            Manufacturer.id <= 3,
            Category_pill.category_id <= 1,
            Pill.price <= 100,
            Category.name.ilike('sedative'),
            ))\
            .all()
