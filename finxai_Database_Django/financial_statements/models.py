from django.db import models
from screener.models import Stock


# Create your models here.
class IncomeStatement(models.Model):
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="income_statements")
    date = models.DateField()
    sales = models.IntegerField(null=True)
    cost_of_goods = models.IntegerField(null=True)
    gross_profit = models.IntegerField(null=True)
    operating_expenses = models.IntegerField(null=True)
    operating_income = models.IntegerField(null=True)
    interest_expense = models.IntegerField(null=True)
    other_income = models.IntegerField(null=True)
    pretax_income = models.IntegerField(null=True)
    income_tax = models.IntegerField(null=True)
    net_income_continuous = models.IntegerField(null=True)
    net_income = models.IntegerField(null=True)
    net_income_discontinuous = models.IntegerField(null=True)
    minority_interests = models.IntegerField(null=True)
    eps_basic_total_ops = models.FloatField(null=True)
    eps_basic_continuous_ops = models.FloatField(null=True)
    eps_diluted_total_ops = models.FloatField(null=True)
    eps_diluted_continuous_ops = models.FloatField(null=True)
    eps_diluted_before_nonrecurring_items = models.FloatField(null=True)
    ebitda = models.IntegerField(null=True)
    eps_basic_discontinuous_ops = models.FloatField(null=True)
    eps_diluted_discontinuous_ops = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker.ticker


class BalanceSheet(models.Model):
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="balance_sheets")
    date = models.DateField()
    cash_cash_equivalents = models.IntegerField(null=True)
    marketable_securities = models.IntegerField(null=True)
    receivables = models.IntegerField(null=True)
    inventories = models.IntegerField(null=True)
    income_taxes_deferred = models.FloatField(null=True)
    other_current_assets = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    ppe_net = models.IntegerField(null=True)
    investments_and_advances = models.IntegerField(null=True)
    intangibles = models.IntegerField(null=True)
    other_noncurrent_assets = models.IntegerField(null=True)
    total_assets = models.IntegerField(null=True)
    short_term_debt = models.IntegerField(null=True)
    accounts_payable_and_accrued_liabilities = models.IntegerField(null=True)
    accrued_expenses = models.FloatField(null=True)
    deferred_revenues = models.IntegerField(null=True)
    long_term_debt = models.IntegerField(null=True)
    other_noncurrent_liabilities = models.IntegerField(null=True)
    total_liabilities = models.IntegerField(null=True)
    shares_outstanding_k = models.IntegerField(null=True)
    common_shares = models.IntegerField(null=True)
    retained_earnings = models.IntegerField(null=True)
    other_shareholders_equity = models.IntegerField(null=True)
    total_liabilities_and_equity = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker.ticker


class CashFlow(models.Model):
    ticker = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="cash_flows")
    date = models.DateField()
    net_income = models.IntegerField(null=True)
    depreciation_amortization = models.IntegerField(null=True)
    income_taxes_deferred = models.IntegerField(null=True)
    accounts_receivable = models.IntegerField(null=True)
    accounts_payable_and_accrued_liabilities = models.IntegerField(null=True)
    other_working_capital = models.IntegerField(null=True)
    other_operating_activity = models.IntegerField(null=True)
    operating_cash_flow = models.IntegerField(null=True)
    change_in_deposits = models.IntegerField(null=True)
    ppe_investments = models.IntegerField(null=True)
    net_acquisitions = models.IntegerField(null=True)
    purchase_of_investment = models.IntegerField(null=True)
    sale_of_investment = models.IntegerField(null=True)
    purchase_sale_intangibles = models.IntegerField(null=True)
    other_investing_activity = models.IntegerField(null=True)
    investing_cash_flow = models.IntegerField(null=True)
    change_in_short_term_borrowing = models.FloatField(null=True)
    debt_issued = models.IntegerField(null=True)
    debt_repayment = models.IntegerField(null=True)
    common_stock_issued = models.FloatField(null=True)
    common_stock_repurchased = models.IntegerField(null=True)
    dividend_paid = models.IntegerField(null=True)
    other_financing_activity = models.IntegerField(null=True)
    financing_cash_flow = models.IntegerField(null=True)
    exchange_rate_effect = models.IntegerField(null=True)
    beginning_cash_position = models.IntegerField(null=True)
    end_cash_position = models.IntegerField(null=True)
    net_cash_flow = models.IntegerField(null=True)
    capital_expenditure = models.IntegerField(null=True)
    free_cash_flow = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker.ticker
