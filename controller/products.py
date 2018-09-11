from controller.base import BaseController
from business_logic.products_bl import ProductBl
from flask import Response
import json


class ProductsController(BaseController):

    def __init__(self, products_bl=None):
        super(ProductsController, self).__init__()
        self.products_bl = products_bl or \
                           ProductBl(self.dal_factory.get_product_dal())
        self.__set_reg_parser_args()

    def post(self):
        new_product = self.req_parser.parse_args()
        result = self.products_bl.create(new_product)
        return Response(response=result,
                        status=201,
                        content_type="application/json")

    def get(self, product_id=None):
        result = self.products_bl.get(product_id)
        if result is not None:
            return Response(response=json.dumps(result),
                            status=200,
                            content_type="application/json")
        else:
            msg = "product with id {} was not found".format(product_id)
            return Response(response={"message": msg},
                            status=404,
                            content_type="application/json")

    def delete(self, product_id):
        pass

    def put(self, product_id):
        pass

    def __set_reg_parser_args(self):
        self.req_parser.add_argument("name", type=str, required=True)
        self.req_parser.add_argument("description", type=str, required=True)
        self.req_parser.add_argument("imported", type=bool, required=True)
        self.req_parser.add_argument("category", type=str, required=True)
        self.req_parser.add_argument("price", type=float, required=True)