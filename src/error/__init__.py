class ProductNotFoundError(BaseException):

    def __init__(self, message):
        super(ProductNotFoundError, self).__init__(message)
        self.message = message


class DataAccessLayerError(BaseException):

    def __init__(self, message, class_name):
        super(DataAccessLayerError, self).__init__(message)
        self.message = message
        self.class_name = class_name
