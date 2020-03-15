import datetime
import pathlib

import pandas as pd


class Orders:
    """
    A class to represent a day of orders

    Attributes
    ----------
    root : str
        Path for data directory where files are stored

    order_lines_file : str
        Path of 'order_lines.csv' which acts as base file for class

    data : pd.Dataframe
        Dataframe containing order data for the date

    date: str
        The date of the orders

    Methods
    -------
    order():
        Returns a data-frame of imported orders for a given day.

    commission():
        Returns a data-frame of imported orders combined with commissions for a given day.

    product_promotion():
        Returns a data-frame of imported orders combined with
        commissions and promotions for a given day.

    validate_date_input(date=):
        Validates the input date from GET request
    """

    def __init__(self, date: str) -> None:
        self.root = pathlib.Path.cwd() / "data"
        order_lines_file = pathlib.Path.joinpath(self.root, "order_lines.csv")
        self.data = pd.read_csv(order_lines_file)
        self.validate_date_input(date)
        self.date = date

    def add_order(self) -> pd.DataFrame:
        """
        Returns a data-frame of imported orders for a given day.

        Returns:
            merged_order_lines_data_by_date: a pandas data-frame of orders
        """
        order_file = pathlib.Path.joinpath(self.root, "orders.csv")
        order_data = pd.read_csv(order_file)
        order_data["date"] = order_data["created_at"].str[:10]
        merged_order_lines_data = self.data.merge(
            order_data, left_on="order_id", right_on="id", how="left"
        )
        merged_order_lines_data_by_date = merged_order_lines_data[
            merged_order_lines_data["date"] == self.date
        ]
        self.validate_order_results(merged_order_lines_data_by_date)

        return merged_order_lines_data_by_date

    def add_commission(self) -> pd.DataFrame:
        """
        Returns a data-frame of imported orders combined with commissions for a given day.

        Returns:
            merged_commission_data: a pandas data-frame of orders + commissions
        """
        commission_file = pathlib.Path.joinpath(self.root, "commissions.csv")
        commission_data = pd.read_csv(commission_file)
        commission_data_by_date = commission_data[commission_data["date"] == self.date]
        merged_commission_data = self.add_order().merge(
            commission_data_by_date,
            left_on="vendor_id",
            right_on="vendor_id",
            how="left",
        )
        return merged_commission_data

    def add_product_promotions(self) -> pd.DataFrame:
        """
        Returns a data-frame of imported orders combined with
        commissions and promotions for a given day.

        Returns:
            merged_commission_data: a pandas data-frame of orders + commissions + promotions
        """
        product_promotion_file = pathlib.Path.joinpath(
            self.root, "product_promotions.csv"
        )
        promo_data = pd.read_csv(product_promotion_file)
        promo_data_by_date = promo_data[promo_data["date"] == self.date]
        merged_product_promo_data_by_date = self.add_commission().merge(
            promo_data_by_date, left_on="product_id", right_on="product_id", how="left"
        )
        return merged_product_promo_data_by_date

    @staticmethod
    def validate_date_input(date: str) -> None:
        """
        Validation of input date from GET request
        """
        try:
            year, month, day = date.split("-")
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            raise ValueError(
                f"'{date}' is not a valid date. Ensure you have entered date in YYYY-MM-DD format"
            )

    def validate_order_results(self, order: pd.DataFrame) -> None:
        """
        Validation that order data is available for given date
        """
        number_of_orders = len(order.index)
        if number_of_orders <= 0:
            raise ValueError(
                f"There were no orders on '{self.date}'. Try a different date"
            )
