import peewee

if __name__ == '__main__':
    # Conector de la base de datos
    try:
        database = peewee.MySQLDatabase(
            'pythondb',
            port=3306,
            user='root',
            passwd='root')

        print('Conexión OK')

    except peewee.OperationalError as err:
        print('No fue posible realizar la conexión.')
        print(err)

    finally:
        # Cerramos la conexión
        print('Conexión finalizada de forma exitosa.')