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


class Author(peewee.Model):
    name = peewee.CharField(max_length=50)

    class Meta:
        database = database
        db_table = 'authors'

    def __str__(self):
        return self.name


class Book(peewee.Model):
    title = peewee.CharField(max_length=50)
    author = peewee.ForeignKeyField(Author, backref='books')
    # Con backref, creamos un nuevo atributo para los objetos de tipo Author
    # Utilizando el atributo backref, podemos acceder a la relación

    class Meta:
        database = database
        db_table = 'books'

    def __str__(self):
        return self.title


if __name__ == '__main__':
    database.drop_tables([Author, Book])
    database.create_tables([Author, Book])

    author1 = Author.create(name='Stephen King')

    book1 = Book.create(title='titulo1', author=author1)
    book2 = Book.create(title='titulo2', author=author1)
    book3 = Book.create(title='titulo3', author=author1)

    # Consultamos el autor a partir de un objeto de tipo libro
    print(book2.author)

    # Consultamos un libro a través de un objeto de tipo Author. Esto lo podemos hacer gracias a backref='books'
    for book in author1.books:
        print(book)