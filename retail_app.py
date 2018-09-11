from flask import Flask
from flask_restful import Api
from controller.products import ProductsController

app = Flask(__name__)
api = Api(app)
api.add_resource(ProductsController, "/products", "/products/<product_id>",
                 endpoint="products")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
