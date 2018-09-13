import config
from data_access.local_fs import products_dal, orders_dal


class DBFactory(object):

    def __init__(self):
        """
        Constructor
        :param type: str, the storage backend type
        """
        self.type = config.CONFIG["storage_backend"]

    def get_product_dal(self):
        if self.type == config.LOCAL_FS_STORAGE:
            return products_dal.ProductsLocalFsDal()
        else:
            msg = "storage_backend type '{}' is invalid or is not " \
                  "currently supported".format(self.type)
            raise Exception(msg)

    def get_orders_dal(self):
        if self.type == config.LOCAL_FS_STORAGE:
            return orders_dal.OrdersLocalFsDal()
        else:
            msg = "storage_backend type '{}' is invalid or is not " \
                  "currently supported".format(self.type)
            raise Exception(msg)