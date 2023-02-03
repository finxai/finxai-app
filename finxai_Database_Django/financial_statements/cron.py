import cfscrape
from bs4 import BeautifulSoup
from .models import IncomeStatement, BalanceSheet, CashFlow
from screener.models import Stock
from important_codes.all_functions import *
import pandas as pd


def financial_statements():
    for stock in Stock.objects.filter(ticker__gte="DE").order_by('ticker'):
        print(stock.ticker)
        income_statement(stock)
        balance_sheet(stock)
        cash_flow(stock)


def income_statement(stock):
    try:
        output_data = []
        for page in [1, 2]:
            url = f"https://www.barchart.com/stocks/quotes/{stock.ticker}/income-statement/annual?reportPage={page}"
            print(url)
            scraper = cfscrape.create_scraper()
            soup = BeautifulSoup(scraper.get(url).content, 'html.parser')
            table = soup.find("table")
            output = {}
            if table:
                rows = table.find_all("tr")
                dates = rows[0].find_all("td")[1:]
                output["date"] = [date.get_text().strip() for date in dates]
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if cols:
                        key = clear_key(cols[0].get_text())
                        values = cols[1:]
                        values = [clear_value(value.get_text()) for value in values]
                        if values.count(None) != len(values):
                            output[key] = values
                df = pd.DataFrame(output)
                output_data += df.to_dict(orient="records")

        for defaults in output_data:
            date = defaults.pop("date")
            date = convert_string_to_date("30-" + date, "%d-%m-%Y")
            for k, v in defaults.items():
                if pd.isna(v):
                    defaults[k] = None
            obj, created = IncomeStatement.objects.update_or_create(ticker=stock, date=date, defaults=defaults)
    except Exception as e:
        print(e)
        with open("logs.log", "a") as f:
            f.write(f"{url} \n {e} \n\n")
        with open("tickers.txt", "a") as f:
            f.write(f"{stock.ticker}\n")


def balance_sheet(stock):
    try:
        output_data = []
        for page in [1, 2]:
            url = f"https://www.barchart.com/stocks/quotes/{stock.ticker}/balance-sheet/annual?reportPage={page}"
            print(url)
            scraper = cfscrape.create_scraper()
            soup = BeautifulSoup(scraper.get(url).content, 'html.parser')
            table = soup.find("table")
            output = {}
            if table:
                rows = table.find_all("tr")
                dates = rows[0].find_all("td")[1:]
                output["date"] = [date.get_text().strip() for date in dates]
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if cols:
                        key = clear_key(cols[0].get_text())
                        values = cols[1:]
                        values = [clear_value(value.get_text()) for value in values]
                        if values.count(None) != len(values):
                            output[key] = values
                df = pd.DataFrame(output)
                output_data += df.to_dict(orient="records")

        for defaults in output_data:
            date = defaults.pop("date")
            date = convert_string_to_date("30-" + date, "%d-%m-%Y")
            for k, v in defaults.items():
                if pd.isna(v):
                    defaults[k] = None
            obj, created = BalanceSheet.objects.update_or_create(ticker=stock, date=date, defaults=defaults)
    except Exception as e:
        print(e)
        with open("logs.log", "a") as f:
            f.write(f"{url} \n {e} \n\n")
        with open("tickers.txt", "a") as f:
            f.write(f"{stock.ticker}\n")


def cash_flow(stock):
    try:
        output_data = []
        for page in [1, 2]:
            url = f"https://www.barchart.com/stocks/quotes/{stock.ticker}/cash-flow/annual?reportPage={page}"
            print(url)
            scraper = cfscrape.create_scraper()
            soup = BeautifulSoup(scraper.get(url).content, 'html.parser')
            table = soup.find("table")
            output = {}
            if table:
                rows = table.find_all("tr")
                dates = rows[0].find_all("td")[1:]
                output["date"] = [date.get_text().strip() for date in dates]
                for row in rows[1:]:
                    cols = row.find_all("td")
                    if cols:
                        key = clear_key(cols[0].get_text())
                        values = cols[1:]
                        values = [clear_value(value.get_text()) for value in values]
                        if values.count(None) != len(values):
                            output[key] = values
                df = pd.DataFrame(output)
                output_data += df.to_dict(orient="records")

        for defaults in output_data:
            date = defaults.pop("date")
            date = convert_string_to_date("30-" + date, "%d-%m-%Y")
            for k, v in defaults.items():
                if pd.isna(v):
                    defaults[k] = None
            obj, created = CashFlow.objects.update_or_create(ticker=stock, date=date, defaults=defaults)
    except Exception as e:
        print(e)
        with open("logs.log", "a") as f:
            f.write(f"{url} \n {e} \n\n")
        with open("tickers.txt", "a") as f:
            f.write(f"{stock.ticker}\n")
