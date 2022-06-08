import time
import argparse
from helpers.connection import conn
from tabulate import tabulate

def InfoCheck(parser:argparse.ArgumentParser):
    sub_parsers = parser.add_subparsers(dest='function')

    # Informacion del ciente. Agregarla en detalle a la tabla.
    parser_info = sub_parsers.add_parser('info')
    parser_info.add_argument('id', type=int)

    # Direccion exacta del cliente.
    parser_address = sub_parsers.add_parser('address')
    parser_address.add_argument('id', type=int)
    parser_address_mode = parser_address.add_mutually_exclusive_group()
    parser_address_mode.add_argument('-c', '--create')
    parser_address_mode.add_argument('-e', '--edit', nargs=2)
    parser_address_mode.add_argument('-r', '--remove')

    # Sistema de pago del cliente.
    parser_pay = sub_parsers.add_parser('pay')
    parser_pay.add_argument('id', type=int)
    parser_pay_mode = parser_pay.add_mutually_exclusive_group()
    parser_pay_mode.add_argument('--add-card', type=int)
    parser_pay_mode.add_argument('--add-account', nargs=2)
    parser_pay_mode.add_argument('-r', '--remove', type=int)

    # Sistema de busqueda para el cliente.
    parser_search = sub_parsers.add_parser('search')
    parser_search.add_argument('id', type=int)
    parser_search.add_argument('-a', action='store_true')
    parser_search.add_argument('-o', type=int)
    parser_search.add_argument('-l', type=int, default=10)

    # Tienda para el cliente.
    parser_store = sub_parsers.add_parser('store')
    parser_store.add_argument('id', type=int)
    parser_store.add_argument('sid', type=int)

    # Carro de compras para el cliente.
    parser_cart = sub_parsers.add_parser('cart')
    parser_cart.add_argument('id', type=int)
    parser_cart_mode = parser_cart.add_mutually_exclusive_group()
    parser_cart_mode.add_argument('-c', type=int, nargs='+')
    parser_cart_mode.add_argument('-p', type=int)
    parser_cart_mode.add_argument('-r', action='store_true')

    # Lista de infomacion para el cliente.
    parser_list = sub_parsers.add_parser('list')
    parser_list.add_argument('id', type=int)
    parser_list.add_argument('-w', '--waiting', action='store_true')

def customerInfo(contenido):
    cur = conn.cursor()
    sql = "SELECT * FROM customer WHERE id=%(id)s;"
    cur.execute(sql, {"id": contenido.id})
    rows = cur.fetchall()
    print("\nCustomer #" + str(contenido.id) + "'s Information:")
    print("--------------------------------------")
    print("Name: " + str(rows[0][1]))
    print("Phone: " + str(rows[0][2]))
    print("Email: " + str(rows[0][3]) + "@" + str(rows[0][4]))
    print("Password: " + str(rows[0][5]))
    print("Payments:\n" + tabulate(rows[0][6], headers="keys", tablefmt='fancy_grid'))
    print("Latitude & Longitude: " + str(rows[0][7]) + "/" + str(rows[0][8]))
    print("--------------------------------------")

def customerAddress(contenido):
    cur = conn.cursor()
    sql = "SELECT * FROM address WHERE cid=%(id)s;"
    cur.execute(sql, {"id": contenido.id})
    rows = cur.fetchall(); rows = sorted(rows)
    print("\nCustomer #" + str(contenido.id) + "'s Address Information:")
    print("-----------------------------------------------------")
    for row in rows:
        print(str(row[0]) + ". " + row[1])
    print("-----------------------------------------------------")

def customerPaymentMethod(contenido):
    cur = conn.cursor()
    sql = "SELECT * FROM customer WHERE id=%(id)s;"
    cur.execute(sql, {"id": contenido.id})
    rows = cur.fetchall()
    print("\nCustomer #" + str(contenido.id) + "'s Payment methods:\n")
    print(tabulate(rows[0][6], headers="keys", showindex="always", tablefmt='fancy_grid'))

if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    InfoCheck(parser)
    contenido = parser.parse_args()

    if contenido.function == "info":
        customerInfo(contenido)

    elif contenido.function == "address":
        if contenido.create is not None:
            cur = conn.cursor()
            sqlMax = "SELECT MAX(id) FROM address;"
            cur.execute(sqlMax)
            maxId = cur.fetchall()
            maxId = maxId[0][0]
            if maxId is None:
                maxId = 0
            maxId += 1
            sqlAdd = "INSERT INTO address(direccion, id, cid) VALUES (%(Direccion)s, %(Did)s, %(Cid)s);"
            cur.execute(sqlAdd, {"Direccion": contenido.create, "Did": maxId, "Cid": contenido.id})
            conn.commit()
            customerAddress(contenido)

        elif contenido.edit is not None:
            cur = conn.cursor()
            sqlEdit = "UPDATE address SET direccion = (%(Direccion)s) WHERE cid = %(Cid)s AND id = %(Did)s;"
            cur.execute(sqlEdit, {"Direccion": contenido.edit[1], "Cid": contenido.id, "Did": contenido.edit[0]})
            conn.commit()
            customerAddress(contenido)

        elif contenido.remove is not None:
            cur = conn.cursor()
            sqlEdit = "DELETE FROM address WHERE cid = %(Cid)s AND id = %(Did)s;"
            cur.execute(sqlEdit, {"Cid": contenido.id, "Did": contenido.remove[0]})
            conn.commit()
            customerAddress(contenido)
        else:
            customerAddress(contenido)

    elif contenido.function == "pay":
        if contenido.add_card is not None:
            newCard = {"data": {"card_num": None}, "type": "card"}
            (newCard["data"])["card_num"] = contenido.add_card
            cur = conn.cursor()
            sql = "SELECT customer.payments FROM customer WHERE customer.id=%(id)s;"
            cur.execute(sql, {"id": contenido.id})
            rows = cur.fetchall(); rows = sorted(rows)
            rows[0][0].append(newCard)
            rowsNew = str(rows[0][0]).replace("\'", "\"")
            sqlAdd = "UPDATE customer SET payments = (%(Payments)s) WHERE id = %(Cid)s;"
            cur.execute(sqlAdd, {"Payments": rowsNew, "Cid": contenido.id})
            conn.commit()
            customerPaymentMethod(contenido)
        elif contenido.add_account is not None:
            newAccount = {"data": {"acc_num": None}, "type": "account"}
            (newAccount["data"])["acc_num"] = contenido.add_account
            cur = conn.cursor()
            sql = "SELECT customer.payments FROM customer WHERE customer.id=%(id)s;"
            cur.execute(sql, {"id": contenido.id})
            rows = cur.fetchall();
            rows = sorted(rows)
            rows[0][0].append(newAccount)
            rowsNew = str(rows[0][0]).replace("\'", "\"")
            sqlAdd = "UPDATE customer SET payments = (%(Payments)s) WHERE id = %(Cid)s;"
            cur.execute(sqlAdd, {"Payments": rowsNew, "Cid": contenido.id})
            conn.commit()
            customerPaymentMethod(contenido)
        elif contenido.remove is not None:
            cur = conn.cursor()
            sql = "SELECT customer.payments FROM customer WHERE customer.id=%(id)s;"
            cur.execute(sql, {"id": contenido.id})
            rows = cur.fetchall();
            rows = sorted(rows)
            rows[0][0].pop(contenido.remove)
            rowsNew = str(rows[0][0]).replace("\'", "\"")
            cur = conn.cursor()
            sqlAdd = "UPDATE customer SET payments = (%(Payments)s) WHERE id = %(Cid)s;"
            cur.execute(sqlAdd, {"Payments": rowsNew, "Cid": contenido.id})
            conn.commit()
            customerPaymentMethod(contenido)
        else:
            customerPaymentMethod(contenido)

    elif contenido == "search":
        cur = conn.cursor()
        sqlSearch = "SELECT lat, lng FROM customer WHERE id = (%(Cid)s);"
        cur.execute(sqlSearch, {"Cid": contenido.id})
        locationInfo = cur.fetchone()
        lat = locationInfo[0]
        longi = locationInfo[1]

        sqlFindRestaurant = "SELECT delivery.id FROM delivery WHERE delivery.stock <= 4 ORDER BY power(((%(Latitude)s)-delivery.lat), 2) + power((%(Longitude)s-delivery.lng), 2) LIMIT 1;"
        cur.execute(sqlFindRestaurant, {"Latitude": lat, "Longitude": longi})
        delivery_id = (cur.fetchone())[0]  # delivery id

    else:
        print("Input Error!")

    print(time.time() - start)

