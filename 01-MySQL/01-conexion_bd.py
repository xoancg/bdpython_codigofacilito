import pymysql

# Constante
DROP_TABLE_USERS = "DROP TABLE IF EXISTS users"
USERS_TABLE = """CREATE TABLE users(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Conector de la base de datos
    try:
        connect = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='pythondb')

        # Usamos el método cursor() para poder ejecutar consultas SQL
        cursor = connect.cursor()
        cursor.execute(DROP_TABLE_USERS)
        cursor.execute(USERS_TABLE)

        print('Conexión OK')

    except pymysql.err.OperationalError as err:
        print('No fue posible realizar la conexión.')
        print(err)

    finally:
        # Cerramos la conexión
        cursor.close()
        connect.close()
        print('Conexión finalizada de forma exitosa.')
