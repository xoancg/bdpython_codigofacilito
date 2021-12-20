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

    # Para trabajar con un objeto de tipo User en lugar de ModelSelect, usamos el método get()
    # get() permite obtener un registro a partir de una consulta
    user = User.select().where(User.id == 1).get()
    print(user)

    user.username = 'new_user1'
    user.email = 'new_user1@correo.com'

    # save() actualiza el registro preexistente o crea uno nuevo si éste no existe
    user.save()

    user = User.select().where(User.id == 1).get()
    print(user)

    # Otra forma: update()
    query = User.update(username='renew_user2',
                        email='renew_user2@correo.com')\
        .where(User.id == 2)
    print(query)  # Imprimimos la consulta SQL
    query.execute()
