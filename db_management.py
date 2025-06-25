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
