import controller as con
from psycopg2 import Error
import sys

c = con.Controller()

try:
    command = sys.argv[1]
except IndexError:
    c.v.no_command()
else:
    if command == 'print_table':
        try:
            name = sys.argv[2]
        except IndexError:
            c.v.argument_error()
        else:
            c.print(name)

    elif command == 'delete_record':
        try:
            args = {"name": sys.argv[2], "val": sys.argv[3]}
        except IndexError:
            c.v.argument_error()
        else:
            c.delete(args["name"], args["val"])

    elif command == 'update_record':
        try:
            args = {"table": sys.argv[2], "key": sys.argv[3]}
            if args["table"] == 'Category':
                args["name"], args["description"] = sys.argv[4], sys.argv[5]
            elif args["table"] == 'Category_pill':
                args["pill_id"], args["category_id"] = sys.argv[4], sys.argv[5]
            elif args["table"] == 'Pill':
                args["manufacturer_id"], args["name"], args["price"] = sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["table"] == 'Manufacturer':
                args["name"], args["country"], args["email"] = sys.argv[4], sys.argv[5], sys.argv[6]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["table"] == 'Category':
                c.update_category(args["key"], args["name"], args["description"])
            elif args["table"] == 'Category_pill':
                c.update_category_pill(args["key"], args["pill_id"], args["category_id"])
            elif args["table"] == 'Pill':
                c.update_pill(args["key"], args["manufacturer_id"], args["name"], args["price"])
            elif args["table"] == 'Manufacturer':
                c.update_manufacturer(args["key"], args["name"], args["country"], args["email"])

    elif command == 'insert_record':
        try:
            args = {"table": sys.argv[2], "key": sys.argv[3]}
            if args["table"] == 'Category':
                args["name"], args["description"] = sys.argv[4], sys.argv[5]
            elif args["table"] == 'Category_pill':
                args["pill_id"], args["category_id"] = sys.argv[4], sys.argv[5]
            elif args["table"] == 'Pill':
                args["manufacturer_id"], args["name"], args["price"] = sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["table"] == 'Manufacturer':
                args["name"], args["country"], args["email"] = sys.argv[4], sys.argv[5], sys.argv[6]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["table"] == 'Category':
                c.insert_category(args["key"], args["name"], args["description"])
            elif args["table"] == 'Category_pill':
                c.insert_category_pill(args["key"], args["pill_id"], args["category_id"])
            elif args["table"] == 'Pill':
                c.insert_pill(args["key"], args["manufacturer_id"], args["name"], args["price"])
            elif args["table"] == 'Manufacturer':
                c.insert_manufacturer(args["key"], args["name"], args["country"], args["email"])

    elif command == 'test':

        print(not c.m.find_product(13))

    elif command == 'generate_randomly':

        try:

            args = {"name": sys.argv[2], "n": int(sys.argv[3])}

        except (IndexError, Exception):

            print(Exception, IndexError)

        else:

            c.generate(args["name"], args["n"])

    elif command == 'search_records':

        while True:

            search_num = c.v.get_search_num()

            try:
                search_num = int(search_num)
            except ValueError:
                c.v.invalid_search_num()
            else:
                if search_num in [2, 3, 4]:

                    break

                else:
                    c.v.invalid_search_num()

        if search_num == 2:
            c.search_two()

        elif search_num == 3:
            c.search_three()

        elif search_num == 4:
            c.search_all()

    elif command == 'help':

        c.v.print_help()
    else:
        c.v.wrong_command()
