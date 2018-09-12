from data_access.local_fs import BaseLocalFsDal
import json
import logging


class ProductsDal(BaseLocalFsDal):

    def __init__(self):
        super(ProductsDal, self).__init__()
        self.products_path = self.base_path + "/products/products.json"
        self.__logger = logging.getLogger(ProductsDal.__name__)
        self.__logger.setLevel(logging.INFO)

    def create(self, product):
        if product is None:
            raise ValueError("product argument cannot be None")

        with open(self.products_path, 'r+') as f:
            content = f.read()
            f.seek(0)
            f.truncate()
            products = json.loads(content)
            products.append(product)
            f.write(json.dumps(products))

    def delete(self, product_id):
        pass

    def get(self, product_id=None):

        with open(self.products_path, 'r') as f:
            content = f.read()
            products = json.loads(content)
            if product_id is not None:
                for p in products:
                    if p["id"] == product_id:
                        return p
                return None
            else:
                return products

    def update(self, product):
        pass
