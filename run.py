from flask import Flask
from flask_restful import Api, Resource

from app.report import DailyShopSummary

app = Flask(__name__)
api = Api(app)


class Shop(Resource):
    def get(self, date):
        try:
            shop_data = DailyShopSummary(date)

            response = {
                "customers": shop_data.total_number_of_customers,
                "items": shop_data.total_number_of_items_sold,
                "order_total_avg": shop_data.average_order_total,
                "discount_rate_ave": shop_data.average_discount_rate,
                "commissions": {
                    "promotions": shop_data.total_commission_per_promotion,
                    "total": shop_data.total_commission,
                    "order_average": shop_data.average_order_commission,
                },
            }

            return response, 200

        except Exception as error:
            return {"message": str(error)}, 400


api.add_resource(Shop, "/<string:date>")

if __name__ == "__main__":
    app.run(debug=True)
