import mysql.connector

def get_order_status(order_id: int):
    try:
        # Always establish a fresh connection
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Door#@mirror555',
            database='pandeyji_eatery'
        )

        cursor = cnx.cursor()
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals() and cnx.is_connected():
            cnx.close()

    return result[0] if result else None


def get_max_order_id():
    try:
        # Establish a new connection
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Door#@mirror555',
            database='pandeyji_eatery'
        )

        cursor = cnx.cursor()
        query = "SELECT MAX(order_id) FROM orders"
        cursor.execute(query)
        result = cursor.fetchone()[0]

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals() and cnx.is_connected():
            cnx.close()

    return result+1 if result is not None else 1


def insert_order_item(food_item, quantity, order_id):
    try:
        # Establish a new connection
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Door#@mirror555',
            database='pandeyji_eatery'
        )

        cursor = cnx.cursor()

        # Call the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # Commit the changes
        cnx.commit()

        print("Order item inserted successfully!")
        return 1

    except mysql.connector.Error as err:
        print(f"MySQL Error inserting order item: {err}")
        cnx.rollback()
        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        cnx.rollback()
        return -1

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals() and cnx.is_connected():
            cnx.close()



def get_total_order_price(order_id):
    try:
        # Establish a fresh connection
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Door#@mirror555',
            database='pandeyji_eatery'
        )

        cursor = cnx.cursor()

        # Executing the SQL query to get the order price using a stored function
        query = f"SELECT get_total_order_price({order_id})"
        cursor.execute(query)

        # Fetching the result
        result = cursor.fetchone()[0]

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals() and cnx.is_connected():
            cnx.close()

    return result

    

import mysql.connector

def insert_order_tracking(order_id, status):
    try:
        # Establish a new connection
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Door#@mirror555',
            database='pandeyji_eatery'
        )

        cursor = cnx.cursor()

        # Inserting the record into the order_tracking table
        insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, status))

        # Committing the changes
        cnx.commit()

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        cnx.rollback()
        return -1

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'cnx' in locals() and cnx.is_connected():
            cnx.close()

    return 1


