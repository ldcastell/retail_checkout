from uuid import uuid4, UUID
import logging


class ProductBl(object):

    def __init__(self, product_dal):
        """
        Constructor
        :param product_dal: products Data Access Layer
        """
        self.dal = product_dal
        self.__logger = logging.getLogger(ProductBl.__name__)
        self.__logger.setLevel(logging.INFO)

    def create(self, product):
        if product is None:
            raise Exception("Product cannot be None")
        product['id'] = str(uuid4())
        self.dal.create(product)
        return product

    def get(self, product_id=None):
        if product_id is not None:
            try:
                UUID(product_id, version=2)
            except ValueError as err:
                msg = "The product_id is not a valid UUID."
                self.__logger.error(msg)
                raise err

        return self.dal.get(product_id)

    def update(self, product):
        if product is None:
            raise Exception("Product cannot be None")
        if "id" in product.keys():
            try:
                UUID(product["id"], version=4)
            except ValueError as err:
                msg = "The product_id is not a valid UUID."
                self.__logger.error(msg)
                raise err
            self.dal.update(product)

    def delete(self, product_id):
        try:
            UUID(product_id, version=2)
        except ValueError as err:
            msg = "The product_id is not a valid UUID."
            self.__logger.error(msg)
            raise err
        self.dal.delete(product_id)
