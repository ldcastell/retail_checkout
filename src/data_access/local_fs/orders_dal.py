import json
import logging

from config import CONFIG
from data_access.local_fs import BaseLocalFsDal
from error import DataAccessLayerError


class OrdersLocalFsDal(BaseLocalFsDal):

    def __init__(self):
        super(OrdersLocalFsDal, self).__init__()
        self.orders_path = self.base_path + "/orders/orders.json"
        self.__logger = logging.getLogger(OrdersLocalFsDal.__name__)
        self.__logger.setLevel(CONFIG["api_log_level"])

    def create(self, order):
        if order is None:
            raise ValueError("product argument cannot be None")

        try:
            with open(self.orders_path, 'r+') as f:
                content = f.read()
                f.seek(0)
                f.truncate()
                orders = json.loads(content)
                orders.append(order)
                f.write(json.dumps(orders))
        except (IOError, FileNotFoundError) as err:
            msg = "Error while trying to save the new order"
            raise DataAccessLayerError(msg, OrdersLocalFsDal.__name__)

    def delete(self, order_id):
        raise NotImplementedError()

    def get(self, order_id=None):

        try:
            with open(self.orders_path, 'r') as f:
                content = f.read()
                orders = json.loads(content)
                if order_id is not None:
                    for order in orders:
                        if order["id"] == order_id:
                            return order
                    return None
                else:
                    return orders
        except (IOError, FileNotFoundError) as err:
            msg = "Error while trying to get the orders"
            raise DataAccessLayerError(msg, OrdersLocalFsDal.__name__)

    def update(self, order):
        raise NotImplementedError()
