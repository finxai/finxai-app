from finvizfinance.screener.overview import Overview
from .models import Stock


def add_stocks():
    foverview = Overview()
    for exchange in ["AMEX", "NASDAQ", "NYSE"]:
        filters_dict = {"Exchange": exchange}
        foverview.set_filter(filters_dict=filters_dict)
        df = foverview.screener_view()
        for i, row in df.iterrows():
            defaults = {"company_name": row["Company"], "exchange": exchange}
            stock, created = Stock.objects.update_or_create(
                ticker=row["Ticker"], defaults=defaults
            )


def update_etf():
    foverview = Overview()
    for exchange in ["AMEX", "NASDAQ", "NYSE"]:
        filters_dict = {"Industry": "Exchange Traded Fund", "Exchange": exchange}
        foverview.set_filter(filters_dict=filters_dict)
        df = foverview.screener_view()
        for i, row in df.iterrows():
            defaults = {"company_name": row["Company"], "exchange": exchange, "is_etf": True}
            stock, created = Stock.objects.update_or_create(
                ticker=row["Ticker"], defaults=defaults
            )