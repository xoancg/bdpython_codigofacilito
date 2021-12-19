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

        # Usando el cursor dentro de este contexto, se cerrará la conexión automáticamente al salir del bloque de código
        # Ya no es necesario cerrar el cursor y la conexión de forma explícita con cursor.close() y connect.close()
        with connect.cursor() as cursor:
            # Usamos el método cursor() para poder ejecutar consultas SQL
            cursor.execute(DROP_TABLE_USERS)
            cursor.execute(USERS_TABLE)

            # Definición de la consulta INSERT
            query = "INSERT INTO  users(username, password, email) VALUES('string', 'pass', 'correo@dominio.com')"
            # Usaremos una tupla de valores
            # values = ("eduardo", "pass", "correo@dominio.com")

            # Ejecutar consulta
            cursor.execute(query)
            # Confirmar cambios
            connect.commit()

        print('Conexión OK')

    except pymysql.err.OperationalError as err:
        print('No fue posible realizar la conexión.')
        print(err)

    finally:
        # Cerramos la conexión
        print('Conexión finalizada de forma exitosa.')
