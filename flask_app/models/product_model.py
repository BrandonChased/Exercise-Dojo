from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE

class Product:
    
    def __init__(self,data):
        self.id = data["id"] 
        self.name = data["name"]
        self.price = data["price"]
        self.url = data["url"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.product_category = data["product_category_id"]

#****************************************************** CREATE METHODS ***********************************************************

#********************* CREATE ON PRODUCT **********************
    @classmethod
    def add_product(cls,data):
        query = """
            INSERT INTO products(name,price,img,description,user_id,product_category)
            VALUES(%(name)s,%(price)s,%(img)s,%(description)s,%(user_id)s,%(product_category_id)s)
        """

        return connectToMySQL(DATABASE).query_db(query,data)


#****************************************************** READ METHODS ***********************************************************

#********************* GET ONE PRODUCT **********************
    @classmethod
    def get_product(cls,data):

        query = """
            SELECT * FROM products
            WHERE id = %(id)s;
        """
        
        results = connectToMySQL(DATABASE).query_db(query,data)

        if results:
            return results[0]

#********************* GET ONE PRODUCT CLS**********************
    @classmethod
    def get_product_cls(cls,data):

        query = """
            SELECT * FROM products
            WHERE id = %(id)s;
        """
        
        results = connectToMySQL(DATABASE).query_db(query,data)

        if results:
            return cls(results[0])

#********************* GET ALL PRODUCTS **********************
    @classmethod
    def get_all_products(cls):

        query = """
            SELECT * FROM products
        """
        
        results = connectToMySQL(DATABASE).query_db(query)

        products = []

        if results:
            for result in results:
                one_product = cls(result)
                products.append(one_product)

            return products
# ********************* GET ALL PRODUCTS IN CATEGORY**********************
    @classmethod
    def get_all_products_in_category(cls,id):

        data = {
            'id' : id
        }

        query = """
            SELECT * FROM products
            WHERE product_category_id = %(id)s;
        """
        
        results = connectToMySQL(DATABASE).query_db(query,data)

        products = []

        if results:
            for result in results:
                one_product = cls(result)
                products.append(one_product)
        return products