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

users = [
    ('user1', 'pass1', 'correo@dominio.com'),
    ('user2', 'pass2', 'correo@dominio.com'),
    ('user3', 'pass3', 'correo@dominio.com'),
    ('user4', 'pass4', 'correo@dominio.com'),
    ('user5', 'pass5', 'correo@dominio.com')
]

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

            # Definición de la consulta INSERT con placeholders
            query = "INSERT INTO  users(username, password, email) VALUES(%s, %s, %s)"

            # Ejecutar consulta
            # for user in users:
            #     cursor.execute(query, user)

            # Consulta múltiple sin usar bucle
            cursor.executemany(query, users)

            # Confirmar cambios en la base de datos
            connect.commit()

            # Devolvemos datos. No es necesario ejecutar commit porque no haremos ningún cambio en la base de datos
            query = "SELECT * FROM users"
            rows = cursor.execute(query)
            for user in cursor.fetchall():
                print(user)

            # Otra consulta más precisa
            query = "SELECT id, username, email FROM users WHERE id >= 3"
            rows = cursor.execute(query)
            for user in cursor.fetchall():
                print(user)

        print('Conexión OK')

    except pymysql.err.OperationalError as err:
        print('No fue posible realizar la conexión.')
        print(err)

    finally:
        # Cerramos la conexión
        print('Conexión finalizada de forma exitosa.')
