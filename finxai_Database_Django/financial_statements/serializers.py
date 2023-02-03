from rest_framework import serializers
from screener.models import Stock
from .models import IncomeStatement, BalanceSheet, CashFlow


class IncomeStatementSerializers(serializers.ModelSerializer):
    class Meta:
        model = IncomeStatement
        fields = ['date', 'sales', 'cost_of_goods', 'gross_profit', 'operating_expenses', 'operating_income',
                  'other_income', 'pretax_income', 'income_tax', 'net_income_continuous', 'net_income',
                  'eps_basic_total_ops', 'eps_basic_continuous_ops', 'eps_diluted_total_ops',
                  'eps_diluted_continuous_ops', 'eps_diluted_before_nonrecurring_items', 'ebitda']


class BalanceSheetSerializers(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheet
        fields = ['date', 'cash_cash_equivalents', 'marketable_securities', 'receivables', 'inventories',
                  'income_taxes_deferred', 'other_current_assets', 'total', 'ppe_net', 'investments_and_advances',
                  'intangibles', 'other_noncurrent_assets', 'total_assets', 'short_term_debt',
                  'accounts_payable_and_accrued_liabilities', 'accrued_expenses', 'deferred_revenues', 'long_term_debt',
                  'other_noncurrent_liabilities', 'total_liabilities', 'shares_outstanding_k', 'common_shares',
                  'retained_earnings', 'other_shareholders_equity', 'total_liabilities_and_equity']


class CashFlowSerializers(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = ['date', 'net_income', 'depreciation_amortization', 'income_taxes_deferred', 'accounts_receivable',
                  'accounts_payable_and_accrued_liabilities', 'other_working_capital', 'other_operating_activity',
                  'operating_cash_flow', 'change_in_deposits', 'ppe_investments', 'net_acquisitions',
                  'purchase_of_investment', 'sale_of_investment', 'other_investing_activity', 'investing_cash_flow',
                  'change_in_short_term_borrowing', 'debt_issued', 'debt_repayment', 'common_stock_issued',
                  'common_stock_repurchased', 'dividend_paid', 'other_financing_activity', 'financing_cash_flow',
                  'beginning_cash_position', 'end_cash_position', 'net_cash_flow', 'capital_expenditure',
                  'free_cash_flow']


class StockSerializers(serializers.ModelSerializer):
    income_statements = IncomeStatementSerializers(many=True, read_only=True)
    balance_sheets = BalanceSheetSerializers(many=True, read_only=True)
    cash_flows = CashFlowSerializers(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ["ticker", "company_name", "exchange", "type", "income_statements", "balance_sheets", "cash_flows"]
