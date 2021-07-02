from mysql.connector import MySQLConnection, Error
from mysql_dbconfig import read_db_config


def query_with_fetchone():
    """
    Queries a row from the Customer table using MySQLQuery.fetchone(). Returns nothing.
    """
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        # MySQLCursor objects interact with the reservation_system via the MySQLConnection object
        cursor = conn.cursor()
        cursor.execute("select * from Customer")

        # fetchone() returns the next row of a query result set or None if there is no row left
        row = cursor.fetchone()

        while row is not None:
            print(row)
            row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def query_with_fetchall():
    """
    Queries a row from the Customer table using MySQLQuery.fetchall(). Returns nothing.
    """
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        # MySQLCursor objects interact with the reservation_system via the MySQLConnection object
        cursor = conn.cursor()
        cursor.execute("select * from Customer")

        # fetchall() returns all rows of a table
        rows = cursor.fetchall()

        print('Total Row(s):', cursor.rowcount)
        for row in rows:
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def iter_row(cursor, size):
    """
    Generator that divides queries into a series of fetchmany() calls.
    """
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row


def query_with_fetchmany():
    """
    Queries a row from the Customer table using the iter_row() generator. Returns nothing.
    """
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        # MySQLCursor objects interact with the reservation_system via the MySQLConnection object
        cursor = conn.cursor()
        cursor.execute("select * from Customer")

        for row in iter_row(cursor, 1):
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    query_with_fetchall()
