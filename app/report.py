from app.shop import Orders


class DailyShopSummary:
    """
    A class to summarise orders on a given day
    """

    def __init__(self, date) -> None:
        order_lines = Orders(date)
        self.promotion_data = order_lines.add_product_promotions()

    @property
    def total_number_of_items_sold(self) -> int:
        """
        Returns the number of items sold on date

        Returns:
            total_number_of_items_sold : an int of total items sold
        """
        return len(self.promotion_data.index)

    @property
    def total_number_of_customers(self) -> int:
        """
        Returns the number of customers on date

        Returns:
            total_number_of_customers : an int of total customers
        """
        return self.promotion_data["customer_id"].nunique()

    @property
    def total_discount(self) -> int:
        """
        Returns the total discount on date

        Returns:
            total_discount : an int of total discount
        """
        return self.promotion_data["discounted_amount"].sum().round(2)

    @property
    def average_discount_rate(self) -> int:
        """
        Returns the average discount on date

        Returns:
            average_discount_rate : an int of average discount
        """
        return self.promotion_data["discount_rate"].mean().round(2)

    @property
    def average_order_total(self) -> int:
        """
        Returns the average order total on date

        Returns:
            average_order_total : an int of average order total
        """
        self.promotion_data.groupby("order_id").mean()
        return self.promotion_data["total_amount"].mean().round(2)

    def add_commission(self) -> None:
        """
        Updates promotion data attribute with 'commission'column
            commission = total_amount * rate
        """
        self.promotion_data["commission"] = (
            self.promotion_data.total_amount * self.promotion_data.rate
        )

    @property
    def total_commission(self) -> None:
        """
        Returns the total commission on date

        Returns:
            total_commission : an int of total commission
        """
        self.add_commission()
        return self.promotion_data["commission"].sum().round(2)

    @property
    def average_order_commission(self):
        """
        Returns the average order commission total on date

        Returns:
            average_order_commission : an int of average order commission
        """
        self.add_commission()
        promotion_data_group = self.promotion_data.groupby("order_id").mean()
        return promotion_data_group["commission"].sum().round(2)

    @property
    def total_commission_per_promotion(self):
        """
        Returns the total commission per promotion

        Returns:
            total_commission_per_promotion :
            an int of total commission per promotion
        """
        self.add_commission()
        promotion_data_promo = self.promotion_data[
            self.promotion_data["promotion_id"].notnull()
        ]
        promotion_data_promo_group = (
            promotion_data_promo.groupby("promotion_id").sum().round(2)
        )
        return promotion_data_promo_group.to_dict()["commission"]
