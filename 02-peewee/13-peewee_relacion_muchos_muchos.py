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


class ProductCategory(peewee.Model):
    # Cruzamos los backref para establecer una relación de muchos-a-muchos
    product = peewee.ForeignKeyField(Product, backref='categories')
    category = peewee.ForeignKeyField(Category, backref='products')

    class Meta:
        database = database
        db_table = 'product_categories'


if __name__ == '__main__':
    database.drop_tables([Product, Category, ProductCategory])
    database.create_tables([Product, Category, ProductCategory])

    ipad = Product.create(title='ipad', price=500.50)
    iphone = Product.create(title='iphone', price=800.00)
    tv = Product.create(title='tv', price=600.00)

    technology = Category.create(title='Technology')
    home = Category.create(title='Home')

    ProductCategory.create(product=ipad, category=technology)
    ProductCategory.create(product=iphone, category=technology)
    ProductCategory.create(product=tv, category=technology)

    ProductCategory.create(product=tv, category=home)

    # Acceder a la relación a través de backref
    # Devolvemos los id
    for product in technology.products:
        print(product)
    # Devolvemos los tipos de objeto
    for product in technology.products:
        print(type(product))
    # Devolvemos los nombres (title)
    for product in technology.products:
        print(product.product)

    # Devolvemos las categorías de la tv: id
    for category in tv.categories:
        print(category)
    # Devolvemos las categorías de la tv: title
    for product_category in tv.categories:
        print(product_category.category)
