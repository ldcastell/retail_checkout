import pytest
import json
import retail_app
import mock

from business_logic.orders_bl import OrdersBl
from controller.orders import OrdersController

from http import HTTPStatus


class OrdersMockDal(object):

    def create(self, oder):
        pass

    def delete(self, order_id):
        pass

    def update(self, order):
        pass

    def get(self, order_id=None):
        pass


class TestOrdersController:

    @pytest.fixture
    def orders(self):
        with open("test/data/orders/test_orders.json") as f:
            return json.loads(f.read())

    @pytest.fixture
    def client(self):
        retail_app.app.testing = True
        retail_app.app.view_functions.clear()
        c = retail_app.app.test_client()
        return c

    def test_post(self, orders, client):
        orders_bl = OrdersBl(orders_dal=OrdersMockDal())

        bl_mock = mock.Mock(wraps=orders_bl)

        retail_app.api.add_resource(OrdersController,
                                    "/orders",
                                    "/orders/<order_id>",
                                    endpoint="orders",
                                    resource_class_args=(bl_mock,))

        for order in orders.keys():
            if order != "bad_order":
                resp = client.post("/orders", json=orders[order])
                resp_json = resp.get_json()

                assert resp.is_json
                assert resp.status_code == HTTPStatus.CREATED
                assert resp_json['sales_tax'] == orders[order]["expected_sales_tax"]
                assert resp_json['total'] == orders[order]["expected_total"]

        assert bl_mock.submit.call_count == 3

    def test_post_bad_product_req(self,orders, client):
        orders_bl = OrdersBl(orders_dal=OrdersMockDal())

        bl_mock = mock.Mock(wraps=orders_bl)

        retail_app.api.add_resource(OrdersController,
                                    "/orders",
                                    "/orders/<order_id>",
                                    endpoint="orders",
                                    resource_class_args=(bl_mock,))

        resp = client.post("/orders", json=orders["bad_order"])
        resp_json = resp.get_json()

        bl_mock.submit.assert_not_called()

        assert resp.is_json
        assert resp_json["message"] == "Product non_existing_product Not Found"
        assert resp.status_code == HTTPStatus.BAD_REQUEST

    def test_post_bad_req(self,orders, client):
        orders_bl = OrdersBl(orders_dal=OrdersMockDal())

        bl_mock = mock.Mock(wraps=orders_bl)

        retail_app.api.add_resource(OrdersController,
                                    "/orders",
                                    "/orders/<order_id>",
                                    endpoint="orders",
                                    resource_class_args=(bl_mock,))

        resp = client.post("/orders", json={"bad": "request"})

        bl_mock.submit.assert_not_called()

        assert resp.is_json
        assert resp.status_code == HTTPStatus.BAD_REQUEST
