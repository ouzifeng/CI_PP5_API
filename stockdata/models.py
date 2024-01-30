from django.db import models

class General(models.Model):
    code = models.CharField(max_length=20)
    type = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    exchange = models.CharField(max_length=50, null=True, blank=True)
    currency_code = models.CharField(max_length=10, null=True, blank=True)
    currency_name = models.CharField(max_length=50, null=True, blank=True)
    currency_symbol = models.CharField(max_length=10, null=True, blank=True)
    country_name = models.CharField(max_length=100, null=True, blank=True)
    country_iso = models.CharField(max_length=10, null=True, blank=True)
    isin = models.CharField(max_length=20, null=True, blank=True)
    primary_ticker = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True
    )
    fiscal_year_end = models.CharField(max_length=50, null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    industry = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    web_url = models.URLField(null=True, blank=True)
    logo_url = models.URLField(null=True, blank=True)
    full_time_employees = models.IntegerField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        if not self.logo_url.startswith('https://eodhd.com'):
            self.logo_url = 'https://eodhd.com' + self.logo_url
        super(General, self).save(*args, **kwargs)


class Description(models.Model):
    general = models.OneToOneField(
        General, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        related_name='general_description'
    )
    text = models.TextField()

    def __str__(self):
        return f"Description for {self.general.name} ({self.general.code})"


class Highlights(models.Model):
    general = models.OneToOneField(
        General,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='highlights'
    )
    market_capitalization = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    ebitda = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    pe_ratio = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    peg_ratio = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    wall_street_target_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    book_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    dividend_share = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    dividend_yield = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    earnings_share = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    eps_estimate_current_year = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    eps_estimate_next_year = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    eps_estimate_next_quarter = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    eps_estimate_current_quarter = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    most_recent_quarter = models.DateField(null=True, blank=True)
    profit_margin = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    operating_margin_ttm = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    return_on_assets_ttm = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    return_on_equity_ttm = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    revenue_ttm = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    revenue_per_share_ttm = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    quarterly_revenue_growth_yoy = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    gross_profit_ttm = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    diluted_eps_ttm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    quarterly_earnings_growth_yoy = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Highlights for {self.general.name} ({self.general.code})"

    
class Valuation(models.Model):
    general = models.OneToOneField(
        General,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='valuation'
    )
    trailing_pe = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    forward_pe = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    price_sales_ttm = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    price_book_mrq = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    enterprise_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    enterprise_value_revenue = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    enterprise_value_ebitda = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Valuation for {self.general.name} ({self.general.code})"

    
    
class Technicals(models.Model):
    general = models.OneToOneField(
        General,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='technicals'
    )
    beta = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    fifty_two_week_high = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    fifty_two_week_low = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    fifty_day_ma = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    two_hundred_day_ma = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    shares_short = models.IntegerField(
        null=True,
        blank=True
    )
    shares_short_prior_month = models.IntegerField(
        null=True,
        blank=True
    )
    short_ratio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    short_percent = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Technicals for {self.general.name} ({self.general.code})"
   
    
class SplitsDividends(models.Model):
    general = models.OneToOneField(
        General,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='splits_dividends'
    )
    forward_annual_dividend_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    forward_annual_dividend_yield = models.DecimalField(
        max_digits=5,
        decimal_places=4
    )
    payout_ratio = models.DecimalField(
        max_digits=10,
        decimal_places=4
    )
    dividend_date = models.DateField()
    ex_dividend_date = models.DateField()
    last_split_factor = models.CharField(max_length=20)
    last_split_date = models.DateField()

    def __str__(self):
        return (
            f"Splits and Dividends for {self.general.name} "
            f"({self.general.code})"
        )
    
    
 
class AnalystRatings(models.Model):
    general = models.OneToOneField(
        General,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='analyst_ratings'
    )
    rating = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        null=True,
        blank=True
    )
    target_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    strong_buy = models.IntegerField(null=True, blank=True)
    buy = models.IntegerField(null=True, blank=True)
    hold = models.IntegerField(null=True, blank=True)
    sell = models.IntegerField(null=True, blank=True)
    strong_sell = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Analyst Ratings for {self.general.name} ({self.general.code})"
    
    
class BalanceSheet(models.Model):
    BALANCE_SHEET_TYPE_CHOICES = [
        ('yearly', 'Yearly'),
        ('quarterly', 'Quarterly'),
    ]
    general = models.ForeignKey(
        General,
        on_delete=models.CASCADE,
        related_name='balance_sheets'
    )
    date = models.DateField()
    filing_date = models.DateField()
    currency_symbol = models.CharField(max_length=10)
    total_assets = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    intangible_assets = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    earning_assets = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    other_current_assets = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    total_liabilities = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    total_stockholder_equity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    deferred_long_term_liabilities = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    other_current_liabilities = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    common_stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    capital_stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    retained_earnings = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    other_liabilities = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    goodwill = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    other_assets = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    cash = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    cash_and_equivalents = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    total_current_liabilities = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    current_deferred_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    net_debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    short_term_debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    short_long_term_debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    short_long_term_debt_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    other_stockholder_equity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    property_plant_equipment = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    total_current_assets = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    long_term_investments = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    net_tangible_assets = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    short_term_investments = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    net_receivables = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    long_term_debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    inventory = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    accounts_payable = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    total_permanent_equity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    noncontrolling_interest_in_consolidated_entity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    temporary_equity_redeemable_noncontrolling_interests = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    accumulated_other_comprehensive_income = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    additional_paid_in_capital = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    common_stock_total_equity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    preferred_stock_total_equity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    retained_earnings_total_equity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    treasury_stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    accumulated_amortization = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    non_current_assets_other = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    deferred_long_term_asset_charges = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    non_current_assets_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    capital_lease_obligations = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    long_term_debt_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    non_current_liabilities_other = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    non_current_liabilities_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    negative_goodwill = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    warrants = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    preferred_stock_redeemable = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    capital_surplus = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    liabilities_and_stockholders_equity = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    cash_and_short_term_investments = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    property_plant_and_equipment_gross = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    property_plant_and_equipment_net = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    accumulated_depreciation = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    net_working_capital = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    net_invested_capital = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    common_stock_shares_outstanding = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )

    type = models.CharField(
        max_length=10,
        choices=BALANCE_SHEET_TYPE_CHOICES,
        default='yearly',
    )

    def __str__(self):
        return f"{self.type.title()} Balance Sheet for {self.general.name} ({self.date})" 


class CashFlow(models.Model):
    CASH_FLOW_TYPE_CHOICES = [
        ('yearly', 'Yearly'),
        ('quarterly', 'Quarterly'),
    ]
    general = models.ForeignKey(
        General,
        on_delete=models.CASCADE,
        related_name='cash_flows'
    )
    date = models.DateField()
    filing_date = models.DateField()
    currency_symbol = models.CharField(max_length=10, blank=True, null=True)
    investments = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    change_to_liabilities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_cashflows_from_investing_activities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_borrowings = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_cash_from_financing_activities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    change_to_operating_activities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    change_in_cash = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    begin_period_cash_flow = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    end_period_cash_flow = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_cash_from_operating_activities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    issuance_of_capital_stock = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    depreciation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    other_cashflows_from_investing_activities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    dividends_paid = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    change_to_inventory = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    change_to_account_receivables = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sale_purchase_of_stock = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    other_cashflows_from_financing_activities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    change_to_netincome = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    capital_expenditures = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    change_receivables = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cash_flows_other_operating = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    exchange_rate_changes = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cash_and_cash_equivalents_changes = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    change_in_working_capital = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    stock_based_compensation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    other_non_cash_items = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    free_cash_flow = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    type = models.CharField(
        max_length=10,
        choices=CASH_FLOW_TYPE_CHOICES,
        default='yearly',
    )

    def __str__(self):
        return f"{self.type.title()} Cash Flow for {self.general.name} ({self.date})"
    

class IncomeStatement(models.Model):
    BALANCE_SHEET_TYPE_CHOICES = [
        ('yearly', 'Yearly'),
        ('quarterly', 'Quarterly'),
    ]
    general = models.ForeignKey(
        General,
        on_delete=models.CASCADE,
        related_name='income_statements'
    )
    date = models.DateField()
    filing_date = models.DateField()
    currency_symbol = models.CharField(max_length=10, null=True, blank=True)
    research_development = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    effect_of_accounting_charges = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    income_before_tax = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    minority_interest = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    selling_general_administrative = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    selling_and_marketing_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    gross_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    reconciled_depreciation = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    ebit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    ebitda = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    depreciation_and_amortization = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    non_operating_income_net_other = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    operating_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    other_operating_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    interest_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    tax_provision = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    interest_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_interest_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    extraordinary_items = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    non_recurring = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    other_items = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    income_tax_expense = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_operating_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cost_of_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_other_income_expense_net = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    discontinued_operations = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_income_from_continuing_ops = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    net_income_applicable_to_common_shares = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    preferred_stock_and_other_adjustments = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    type = models.CharField(
        max_length=10,
        choices=BALANCE_SHEET_TYPE_CHOICES,
        default='yearly',
    )

    def __str__(self):
        return f"{self.type.title()} Income Statement for {self.general.name} ({self.date})"
    
    
class CAGR(models.Model):
    general = models.OneToOneField(
        General, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        related_name='general_cagr'
    )
    total_revenue_cagr = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    gross_profit_cagr = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    net_income_cagr = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return f"CAGR for {self.general.name} ({self.general.code})"
