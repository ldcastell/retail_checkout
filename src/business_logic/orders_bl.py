import logging
import math
import uuid


class OrdersBl(object):

    def __init__(self, orders_dal=None):
        """
        Constructor
        :param orders_dal: Orders Data Access Layer
        """
        self.__logger = logging.getLogger(OrdersBl.__name__)
        self.dal = orders_dal

    def submit(self, new_order, products):
        """
        Submits a purchase order and returns a receipt with the purchase details
        :param products: list List of products (list of dictionaries)
        to purchase
        :param new_order:
        :return: dict Receipt with the summary
        """
        if new_order is None or new_order == {}:
            raise ValueError("new_order argument must not be None or Emtpy")
        if products is None or len(products) == 0:
            raise ValueError("products argument must not be None or Empty")

        new_order["id"] = str(uuid.uuid4())
        receipt = dict()
        if products:
            self.__logger.info("Saving Order information to DB")
            self.dal.create(new_order)
            self.__logger.info("Creating the receipt")

            receipt = self.get_receipt(products)
            receipt["order_id"] = new_order["id"]

        return receipt

    def get(self, order_id=None):
        return self.dal.get(order_id)

    @staticmethod
    def get_receipt(products):
        receipt = dict()

        if products is None or len(products) ==0:
            return {}

        receipt["products"] = products
        receipt["sales_tax"] = 0.0
        receipt["total"] = 0.0
        total_products = 0.0
        for product in products:
            if product["category"] not in ["food", "medicine", "book"]:
                receipt["sales_tax"] += (product["price"] *
                                         product["quantity"]) * 0.1
            if product["imported"]:
                receipt["sales_tax"] += (product["price"] *
                                         product["quantity"]) * 0.05
            total_products += product["price"] * product["quantity"]

        # Round up sales tax
        receipt["sales_tax"] = math.ceil(receipt["sales_tax"] / 0.05) * 0.05
        receipt["sales_tax"] = float("{0:.2f}".format(receipt["sales_tax"]))
        receipt["total"] = float("{0:.2f}".format(total_products +
                                                  receipt["sales_tax"]))
        return receipt
