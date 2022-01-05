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

    # Productos sin categoría
    Product.create(title='Product1', price=600.00)
    Product.create(title='Product2', price=600.00)
    Product.create(title='Product3', price=600.00)

    # Listar en consola todos los productos que no posean una categoría
    # Left Join

    products = Product.select(
        Product.title
    ).join(
        ProductCategory,  # Primer argumento: modelo a partir del cual queremos hacer el join
        peewee.JOIN.LEFT_OUTER  # 2º arg.: Especificamos el tipo de join: LEFT JOIN (por defecto, siempre es INNER JOIN)
    ).where(
        ProductCategory.id == None  # No vale: ProductCategory.id is None
    )

    # Imprimimos la consulta
    print(products)
    # Output: SELECT `t1`.`title` FROM `products` AS `t1` LEFT OUTER JOIN `product_categories` AS `t2` ON (
    # `t2`.`product_id` = `t1`.`id`) WHERE (`t2`.`id` IS NULL)

    for product in products:
        print(product.title)

    # Output:
    # Product1
    # Product2
    # Product3
