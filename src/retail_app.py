from flask import Flask, render_template
from flask_restful import Api

from config import CONFIG
from controller.orders import OrdersController
from controller.products import ProductsController

app = Flask(__name__)
api = Api(app)
api.add_resource(ProductsController, "/products", "/products/<product_id>",
                 endpoint="products")
api.add_resource(OrdersController,
                 "/orders",
                 "/orders/<order_id>",

                 endpoint="orders")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(CONFIG["api_port"]))
