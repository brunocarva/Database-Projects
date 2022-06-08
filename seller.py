import time
import argparse
from helpers.connection import conn


def showSellerInfo(sellerInfo):
    print("---------------------------")
    email = str(sellerInfo[0][3]) + "@" + str(sellerInfo[0][4])
    print("Name: " + str(sellerInfo[0][1]))
    print("Phone: " + str(sellerInfo[0][2]))
    print("Email: " + str(email))
    print("---------------------------")


def updateSellerinfo(args, cur):
    sellerId = args.property[0]
    property = args.property[1]

    if property == 'name':
        print("CHANGE NAME!!")
        newName = args.property[2]
        sqlUpdate = "UPDATE seller SET name=%(name)s WHERE id=%(id)s;"
        cur.execute(sqlUpdate, {"name": newName, "id": sellerId})
        conn.commit()
        cur = conn.cursor()
        sql = "SELECT * FROM seller WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.property[0]})
        rows = cur.fetchall()
        showSellerInfo(rows)

    elif property == 'phone':
        print("CHANGE PHONE!!")
        newPhone = args.property[2]
        sqlUpdate = "UPDATE seller SET phone=%(phone)s WHERE id=%(id)s;"
        cur.execute(sqlUpdate, {"phone": newPhone, "id": sellerId})
        conn.commit()
        cur = conn.cursor()
        sql = "SELECT * FROM seller WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.property[0]})
        rows = cur.fetchall()
        showSellerInfo(rows)


    elif property == 'email':
        newLocal = args.property[2]
        newDomain = args.property[3]
        sqlUpdate = "UPDATE seller SET local=%(local)s WHERE id=%(id)s;"
        cur.execute(sqlUpdate, {"local": newLocal, "id": sellerId})
        conn.commit()
        sqlUpdate = "UPDATE seller SET domain=%(domain)s WHERE id=%(id)s;"
        cur.execute(sqlUpdate, {"domain": newDomain, "id": sellerId})
        conn.commit()
        cur = conn.cursor()
        sql = "SELECT * FROM seller WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.property[0]})
        rows = cur.fetchall()
        showSellerInfo(rows)

    elif property == 'password':
        print("CHANGE PASSWORD!!")
        newPass = args.property[2]
        sqlUpdate = "UPDATE seller SET passwd=%(passwd)s WHERE id=%(id)s;"
        cur.execute(sqlUpdate, {"passwd": newPass, "id": sellerId})
        conn.commit()
        cur = conn.cursor()
        sql = "SELECT * FROM seller WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.property[0]})
        rows = cur.fetchall()
        showSellerInfo(rows)

    else:
        print("ERROR! WRONG OPTION!")
        return 0


def main(args):
    id = str(args.id)

    try:
        cur = conn.cursor()
        sql = "SELECT * FROM seller WHERE id=%(id)s;"
        cur.execute(sql, {"id": args.property[0]})
        rows = cur.fetchall()

        if id == 'info':
            showSellerInfo(rows)

        elif id == 'update':
            updateSellerinfo(args, cur)
            cur.execute(sql, {"id": args.property[0]})
            newRows = cur.fetchall()
            print("NEW INFO --> " + str(newRows))
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
