import time
import argparse
from helpers.connection import conn
from tabulate import tabulate


def showStoreInfo(storeInfo):
    print("\nStore #" + str(storeInfo[0][0]) + "'s Info:")
    print("----------------------------------------------------")
    print("Store's Name: " + str(storeInfo[0][2]))
    print("Store's Address: " + str(storeInfo[0][1]))
    print("Store's Phone Numbers: ")
    for phoneNumber in storeInfo[0][5]:
        print("#" + str(storeInfo[0][5].index(phoneNumber)) + " --> " + phoneNumber)
    print("Store Seller's ID: " + str(storeInfo[0][7]))
    print("Store's longitude: " + str(storeInfo[0][3]) + " \nStore's Latitude: " + str(storeInfo[0][4]))
    print("Store's Schedule:")
    print(tabulate(storeInfo[0][6], headers="keys", tablefmt='fancy_grid', missingval=' '))
    print("----------------------------------------------------")


def storeMenu(storeInfo, cur):
    print("Store #" + str(storeInfo[0][0]) + "'s Menu:")
    print("--------------------------------------------")
    sqlStore = "SELECT * FROM Menu AS Me, Store AS S WHERE Me.sid = S.id AND S.id=%(id)s;"
    cur.execute(sqlStore, {"id": storeInfo[0][0]})
    rows = cur.fetchall()
    for row in rows:
        print("#" + str(rows.index(row) + 1) + ". Menu ID: " + str(row[0]) + ", Menu: " + str(row[1]))

    print("--------------------------------------------")


def addMenu(args, storeInfo, cur):
    #print(args.property[1])
    sqlMax = "SELECT MAX(id) FROM menu;"
    cur.execute(sqlMax)
    maxId = cur.fetchall()
    maxId = maxId[0][0]
    maxId += 1
    #print(maxId)
    sqlAdd = "INSERT INTO menu(menu, sid) VALUES (%(Menu)s, %(Sid)s);"
    cur.execute(sqlAdd, {"Menu": args.property[1], "Sid": args.property[0]})
    conn.commit()
    storeMenu(storeInfo, cur)


def main(args):
    id = str(args.id)

    try:
        cur = conn.cursor()
        sql = "SELECT * FROM store WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.property[0]})
        rows = cur.fetchall()

        if id == 'info':
            showStoreInfo(rows)

        elif id == 'menu':
            storeMenu(rows, cur)

        elif id == 'add_menu':
            addMenu(args, rows, cur)

        else:
            parser.print_help()
    except Exception as err:
        print(err)


if __name__ == "__main__":
    start = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help="ID of Seller")
    parser.add_argument("property", nargs=argparse.REMAINDER, help="Property to Change")
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
