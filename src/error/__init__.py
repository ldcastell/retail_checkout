class ProductNotFoundError(BaseException):

    def __init__(self, message):
        super(ProductNotFoundError, self).__init__(message)
        self.message = message
