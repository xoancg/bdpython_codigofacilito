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

    # Creamos una instancia (un objeto) del modelo para poder usarlo
    user1 = User(username='user1', email='user1@dominio.com', active=True)
    # Imprimimos lo que tengamos en el método __str__ de la clase User
    print(user1.active)

    user2 = User()
    user2.username = 'user2'
    user2.email = 'user2@dominio.com'

    # Persistimos los datos. save() es un método de instancia, por lo que necesitamos crear un objeto para usarlo
    user1.save()
    user2.save()

    # Otra forma de llevar a cabo la persistencia: diccionario
    values = {
        'username': 'user3',
        'email': 'user3@dominio.com'
    }

    # Doble asterisco para indicarle a Python que el contenido de las llaves (values) serán los parámetros
    user3 = User(**values)
    user3.save()

    # create() es un método de clase (no de instancia). Podemos ejecutarlo directamente a través del modelo.
    # Create() retorna un objeto
    user4 = User.create(username='user4', email='user4@correo.com')
    # Imprimimos el id para comprobar que se ha registrado en la base de datos
    print(user4.id)

    # Insert también es un método de clase, por lo que no necesitamos ningún objeto.
    # Insert retorna un objeto QUERY (la sentencia SQL)
    query = User.insert(username='user5', email='user5@correo.com')
    print(type(query))  # Devuelve el tipo de objeto: ModelInsert
    query.execute()  # Este método se puede usar siempre que no necesitamos ningún objeto
#