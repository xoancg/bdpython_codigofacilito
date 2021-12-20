import peewee
from datetime import datetime

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


class User(peewee.Model):
    username = peewee.CharField(max_length=50, unique=True, index=True)
    email = peewee.CharField(max_length=50, null=False, unique=True, index=True)
    active = peewee.BooleanField(default=False)
    created_at = peewee.DateTimeField(default=datetime.now())

    class Meta:
        database = database
        db_table = 'users'

    def __str__(self):
        return self.username


if __name__ == '__main__':
    # Si ya existe la tabla, la eliminamos; si no, la creamos
    if User.table_exists():
        User.drop_table()

    User.create_table()

    # Creamos una lista de diccionarios. Cada diccionario tiene los datos de un usuario
    users = [
        {'username': 'user1', 'email': 'user1@correo.com', 'active': True},
        {'username': 'user2', 'email': 'user2@correo.com'},
        {'username': 'user3', 'email': 'user3@correo.com', 'active': True},
        {'username': 'user4', 'email': 'user4@correo.com'},
        {'username': 'user5', 'email': 'user5@correo.com'},
        {'username': 'user6', 'email': 'user6@correo.com', 'active': True},
        {'username': 'user7', 'email': 'user7@correo.com', 'active': True},
    ]

    # El método que usamos para crear varios registros recibe el listado de usuarios por parámetro
    query = User.insert_many(users)
    query.execute()

    # El método select() retorna objeto ModelSelect - Count devuelve el número de registros que devuelve la consulta
    count = User.select().where(User.username == 'user77').count()
    print(count)
    if count > 0:
        print('Existe el usuario consultado.')
    else:
        print('No existe el usuario consultado.')

    # Otro método: exists() - Devuelve valor booleano: True si la consulta retorna algún registro
    exists = User.select().where(User.username == 'user7').exists()
    if exists:
        print('Existe el usuario consultado..')
    else:
        print('No existe el usuario consultado..')