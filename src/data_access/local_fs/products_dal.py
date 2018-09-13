import json
import logging

from data_access.local_fs import BaseLocalFsDal
from error import DataAccessLayerError


class ProductsLocalFsDal(BaseLocalFsDal):

    def __init__(self):
        super(ProductsLocalFsDal, self).__init__()
        self.products_path = self.base_path + "/products/products.json"
        self.__logger = logging.getLogger(ProductsLocalFsDal.__name__)
        self.__logger.setLevel(logging.INFO)

    def create(self, product):
        if product is None:
            raise ValueError("product argument cannot be None")

        try:
            with open(self.products_path, 'r+') as f:
                content = f.read()
                f.seek(0)
                f.truncate()
                products = json.loads(content)
                products.append(product)
                f.write(json.dumps(products))
        except (IOError, FileNotFoundError) as err:
            msg = "Error while trying to save the new product"
            raise DataAccessLayerError(msg, ProductsLocalFsDal.__name__)

    def delete(self, product_id):
        raise NotImplementedError()

    def get(self, product_id=None):

        try:
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
        except (IOError, FileNotFoundError) as err:
            msg = "Error while trying to get the product(s)"
            raise DataAccessLayerError(msg, ProductsLocalFsDal.__name__)

    def update(self, product):
        raise NotImplementedError()
