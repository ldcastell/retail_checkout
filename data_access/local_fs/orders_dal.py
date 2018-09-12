from data_access.local_fs import BaseLocalFsDal
import json
import logging
from config import CONFIG


class OrdersLocalFsDal(BaseLocalFsDal):

    def __init__(self):
        super(OrdersLocalFsDal, self).__init__()
        self.orders_path = self.base_path + "/orders/orders.json"
        self.__logger = logging.getLogger(OrdersLocalFsDal.__name__)
        self.__logger.setLevel(CONFIG["api_log_level"])

    def create(self, order):
        if order is None:
            raise ValueError("product argument cannot be None")

        with open(self.orders_path, 'r+') as f:
            content = f.read()
            f.seek(0)
            f.truncate()
            orders = json.load(content)
            orders.append(order)
            f.write(json.dump(orders))

    def delete(self, order_id):
        pass

    def get(self, order_id=None):

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

    def update(self, order):
        pass
