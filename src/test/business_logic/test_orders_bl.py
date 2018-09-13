import json

import pytest

from business_logic.orders_bl import OrdersBl

import mock

from error import DataAccessLayerError

class OrdersMockDal(object):

    def create(self, oder):
        pass

    def delete(self, order_id):
        pass

    def update(self, order):
        pass

    def get(self, order_id=None):
        pass


class TestOrdersBl:

    @pytest.fixture
    def orders_bl(self):
        orders_bl = OrdersBl(orders_dal=OrdersMockDal())
        return orders_bl

    @pytest.fixture
    def orders(self):
        with open("test/data/orders/test_orders.json") as f:
            return json.loads(f.read())

    @staticmethod
    def get_test_products_from_order(order):
        result = list()
        with open("test/data/products/test_products.json", "r") as f:
            products = json.loads(f.read())
            for p in products:
                if p["id"] in order["products"].keys():
                    p["quantity"] = order["products"][p["id"]]
                    result.append(p)

        return result

    def test_submit_valid_orders(self, orders, orders_bl):
        for order in orders:
            if order != "bad_order":
                products = self.get_test_products_from_order(orders[order])
                receipt = orders_bl.submit(orders[order], products)

                assert receipt is not None

                assert receipt != {}

                assert receipt["sales_tax"] == \
                    orders[order]["expected_sales_tax"]

                assert "order_id" in receipt.keys()

                assert receipt["total"] == orders[order]["expected_total"]

    def test_submit_error_dal(self, orders):
        orders_bl = OrdersBl(orders_dal=mock.Mock(wraps=OrdersMockDal()))
        orders_bl.dal.create.side_effect = \
            DataAccessLayerError("Error in DAL", TestOrdersBl.__name__)
        with pytest.raises(DataAccessLayerError):
            products = self.get_test_products_from_order(orders["order_3"])
            result = orders_bl.submit(orders["order_3"], products)
            assert result is None

    def test_submit_invalid_input(self, orders, orders_bl):
        with pytest.raises(ValueError):
            result = orders_bl.submit(orders["order_3"], [])
            assert result is None
        products = self.get_test_products_from_order(orders["order_3"])
        with pytest.raises(ValueError):
            result2 = orders_bl.submit({}, products)
            assert result2 is None

    def test_get_receipt_valid_products(self, orders, orders_bl):
        products = self.get_test_products_from_order(orders["order_3"])
        result = orders_bl.get_receipt(products)
        assert result is not None and len(result) > 0
        assert result["sales_tax"] == orders["order_3"]["expected_sales_tax"]
        assert result["total"] == orders["order_3"]["expected_total"]

    def test_get_receipt_invalid_products(self, orders, orders_bl):
        products = []
        result = orders_bl.get_receipt(products)
        assert len(result) == 0