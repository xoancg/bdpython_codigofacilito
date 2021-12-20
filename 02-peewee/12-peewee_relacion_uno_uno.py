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
    username = peewee.CharField(max_length=50)
    email = peewee.CharField(max_length=50)

    class Meta:
        database = database
        db_table = 'users'

    def __str__(self):
        return self.username

    @property  # Para tratar al método como un atributo, de forma que podamos llamar a user1.admin
    def admin(self):
        return self.admins.first()


class Admin(peewee.Model):
    permission_level = peewee.IntegerField(default=1)
    user = peewee.ForeignKeyField(User, backref='admins', unique=True)
    # Evitamos que el usuario pueda tener más de un administrador (relación uno-a-uno)
    # Con backref, creamos un nuevo atributo para los objetos de tipo User
    # Utilizando el atributo backref, podemos acceder a la relación

    class Meta:
        database = database
        db_table = 'admins'

    def __str__(self):
        return 'Admin ' + str(self.id)


if __name__ == '__main__':
    database.drop_tables([User, Admin])
    database.create_tables([User, Admin])

    user1 = User.create(username='user1', email='user1@correo.com')
    admin1 = Admin.create(permission_level=10, user=user1)

    # Accedemos a la relación desde Admin
    print(admin1.user)

    # Accedemos al administrador a partir del usuario
    print(user1.admins.first())

    # Otra forma más correcta
    print(user1.admin)

    # Nuevo admin - Da error porque ya existe el usuario user1
    # admin2 = Admin.create(permission_level=5, user=user1)
