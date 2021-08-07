from mysql.connector import MySQLConnection, Error
from MySQLConnection.mysql_dbconfig import read_db_config


def insert_customer(customer_id, customer_name, phone_num, email, address):
    """
    Inserts a customer into the customer table.
    :param customer_id: 
    :param customer_name: 
    :param phone_num: 
    :param email: 
    :param address: 
    :return: 
    """
    query = "insert into customer (customer_id, customer_name, phone_num, email, address)" \
            " values(%s,%s,%s,%s,%s)"
    args = (customer_id, customer_name, phone_num, email, address)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        # cursor.executemany inserts more than one row
        cursor.execute(query, args)

        conn.commit()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def update_customer(customer_id, phone_num):
    """
    Updates a customer's phone number in the customer table.
    :param customer_id:
    :param phone_num:
    :return: 
    """
    
    # read database config
    db_config = read_db_config()
    
    # prepare query
    query = "update customer " \
            "set phone_num = %s" \
            "where customer_id = %s"
    data = (repr(phone_num), repr(customer_id))

    try:
        conn = MySQLConnection(**db_config)
        
        # update customer phone number
        cursor = conn.cursor()
        cursor.execute(query, data)
        
        # accept the changes
        conn.commit()
        
    except Error as e:
        print(e)
    
    finally:
        cursor.close()
        conn.close()


def delete_customer(customer_id):
    db_config = read_db_config()

    query = "DELETE FROM customer WHERE customer_id = %s"

    try:
        # connect to the database server
        conn = MySQLConnection(**db_config)

        # execute the query
        cursor = conn.cursor()
        cursor.execute(query, (customer_id,))

        # accept the change
        conn.commit()

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


def main():
    update_customer(19995, 4158461495)


if __name__ == '__main__':
    main()


