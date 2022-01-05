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
        return 'Título: ' + self.title


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

    # Mostrar en consola todos los productos con sus correspondientes categorias - Problema N+1 Query
    # backref='categories' en ProductCategory.product para acceder a la relación entre un producto y ProductCategory
    # Una forma de hacerlo (no es la mejor, ya que surge el problema de N+1 Query; perdemos el control del nº consultas)

    # Primera consulta: iteramos sobre todos los registros de la tabla Product
    print('\nConsulta generando el problema N+1 Query (demasiadas consultas para bases de datos grandes):')
    for product in Product.select():
        # Segunda consulta de todos los registros de la tabla products (una por cada product_category)
        for product_category in product.categories:
            print(product, '-', product_category.category)

    print('\nUna única consulta utilizando joins:')

    # Para solucionar el problema de N+1 Query, utilizaremos los Joins
    for product in Product.select(
            Product.title, Category.title
    ).join(
        ProductCategory  # Modelo a partir del cual queremos hacer la unión
    ).join(Category,
           on=(  # Segundo join: ProductCategory con Category
                   ProductCategory.category_id == Category.id  # Condiciones de consulta
            )
           ):
        # product.<primer join>.<segundo join> en minúsculas!
        # category.title llama al método __str__ de la clase Category - ¡Esto no funciona aquí! (¿Por qué?)
        print(product, '-', product.productcategory.category.title)
