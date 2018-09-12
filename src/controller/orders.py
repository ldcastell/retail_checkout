import json
import logging
from http import HTTPStatus

from flask import Response

from business_logic.orders_bl import OrdersBl
from config import CONFIG
from controller.base import BaseController
from error import ProductNotFoundError
from flask import request

class OrdersController(BaseController):

    def __init__(self, orders_bl=None):
        super(OrdersController, self).__init__()
        self.__logger = logging.getLogger(OrdersController.__name__)
        self.__logger.setLevel(CONFIG["api_log_level"])
        self.__set_req_args()
        self.orders_bl = orders_bl or \
                         OrdersBl(self.dal_factory.get_orders_dal())
        self.products_dal = self.dal_factory.get_product_dal()

    def post(self):
        new_order = self.req_parser.parse_args()
        try:
            products = self.__get_products_from_order(new_order)
        except ProductNotFoundError as err:
            return Response(response=json.dumps({"message": err.message}),
                            status=HTTPStatus.BAD_REQUEST,
                            content_type="application/json")

        receipt = self.orders_bl.submit(new_order, products)
        return Response(response=json.dumps(receipt),
                        status=HTTPStatus.CREATED,
                        content_type="application/json")

    def get(self, order_id=None):
        try:
            if order_id:
                order = self.orders_bl.get(order_id)

                if order is None:
                    msg = {"message": "Order Not Found"}
                    return Response(response=json.dumps(msg),
                                    status=HTTPStatus.NOT_FOUND,
                                    content_type="application/json")
                return Response(response=json.dumps(order),
                                status=HTTPStatus.OK,
                                content_type="application/json")
            else:
                orders = self.orders_bl.get()
                return Response(response=json.dumps(orders),
                                status=HTTPStatus.OK,
                                content_type="application/json")
        except Exception as err:
            msg = {"message": "There was an error while getting the order(s)"}
            self.__logger.error(err)
            return Response(response=json.dumps(msg),
                            status=HTTPStatus.INTERNAL_SERVER_ERROR,
                            content_type="application/json")

    def get_receipt(self, order_id):
        order = self.orders_bl(order_id)
        if order is None:
            msg = {"message": "Order Not Found"}
            return Response(response=json.dumps(msg),
                            status=HTTPStatus.NOT_FOUND,
                            content_type="application/json")
        try:
            products = self.__get_products_from_order(order)
        except ProductNotFoundError as err:
            return Response(response=json.dumps({"message": err.message}),
                            status=HTTPStatus.BAD_REQUEST,
                            content_type="application/json")

        receipt = self.orders_bl.get_receipt(products)

        if len(receipt) == 0:
            msg = {"message": "Could not find a receipt for the provided order"}
            return Response(response=json.dumps(msg),
                            status=HTTPStatus.NOT_FOUND,
                            content_type="application/json")
        receipt["order_id"] = order_id
        return Response(response=json.dumps(receipt),
                        status=HTTPStatus.OK,
                        content_type="application/json")

    def __set_req_args(self):
        self.req_parser.add_argument("id", type=str)
        self.req_parser.add_argument("products", type=dict, required=True,
                                     location="json")

    def __get_products_from_order(self, order):
        products = list()
        for product_id in order["products"].keys():
            p = self.products_dal.get(product_id)
            if p is None:
                msg = "Product " + product_id + " Not Found"
                self.__logger.error(msg)
                raise ProductNotFoundError(msg)

            else:
                p["quantity"] = order["products"][product_id]
                products.append(p)
        return products
