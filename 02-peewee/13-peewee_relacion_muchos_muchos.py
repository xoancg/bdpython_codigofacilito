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


class Product(peewee.Model):
    title = peewee.CharField(max_length=50)
    price = peewee.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        database = database
        db_table = 'products'

    def __str__(self):
        return self.title


class Category(peewee.Model):
    title = peewee.CharField(max_length=50)

    class Meta:
        database = database
        db_table = 'categories'

    def __str__(self):
        return self.title


if __name__ == '__main__':
    database.drop_tables([Product, Category])
    database.create_tables([Product, Category])

    ipad = Product.create(title='ipad', price=500.50)
    iphone = Product.create(title='iphone', price=800.00)
    tv = Product.create(title='tv', price=600.00)

    tech = Category.create(title='Tech')
    home = Category.create(title='Home')

