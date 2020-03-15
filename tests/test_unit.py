import os
import pathlib

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from app.report import DailyShopSummary
from app.shop import Orders


os.chdir(pathlib.Path.cwd() / "tests")


class TestOrders:

    test_order_df = pd.read_csv(
        pathlib.Path.cwd() / "test_results/test_merged_order_data.csv"
    )
    test_commission_df = pd.read_csv(
        pathlib.Path.cwd() / "test_results/test_merged_commission_data.csv"
    )
    test_promotion_df = pd.read_csv(
        pathlib.Path.cwd() / "test_results/test_merged_promotion_data.csv"
    )

    def setup(self):
        """
        Setup a instance of class Orders for testing
        """
        self.test_order_data = Orders("2019-08-01")
        self.test_shop_data = DailyShopSummary("2019-08-01")

    def test_order(self):
        test_order = self.test_order_data.add_order()
        assert_frame_equal(test_order, self.test_order_df)

    def test_commission(self):
        test_commission = self.test_order_data.add_commission()
        assert_frame_equal(test_commission, self.test_commission_df)

    def test_promotion(self):
        test_commission = self.test_order_data.add_product_promotions()
        assert_frame_equal(test_commission, self.test_promotion_df)

    def test_total_number_of_customers(self):
        customers = self.test_shop_data.total_number_of_customers
        assert customers == 8

    def test_total_number_of_items(self):
        items = self.test_shop_data.total_number_of_items_sold
        assert items == 99


class TestDailyShopSummary:
    def setup(self):
        """
        Setup a instance of class DailyShopSummary for testing
        """
        self.test_shop_data = DailyShopSummary("2019-08-01")

    def test_total_number_of_customers(self):
        customers = self.test_shop_data.total_number_of_customers
        assert customers == 8

    def test_total_number_of_items(self):
        items = self.test_shop_data.total_number_of_items_sold
        assert items == 99

    def test_average_order_total(self):
        order_total_avg = self.test_shop_data.average_order_total
        assert order_total_avg == 1137322.28

    def test_average_discount_rate(self):
        discount_rate_avg = self.test_shop_data.average_discount_rate
        assert discount_rate_avg == 0.13

    def test_total_commission_per_month(self):
        total_commission_per_promotion = (
            self.test_shop_data.total_commission_per_promotion
        )
        assert total_commission_per_promotion == {5.0: 1153804.8}

    def test_total_commission(self):
        total_commission = self.test_shop_data.total_commission
        assert total_commission == 18700917.12

    def test_average_order_commission(self):
        average_order_commission = self.test_shop_data.average_order_commission
        assert average_order_commission == 1341402.46


if __name__ == "__main__":
    pytest.main()
