from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

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
    uid = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True
    )
    primary_ticker = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    fiscal_year_end = models.CharField(max_length=50, null=True, blank=True)
    sector = models.CharField(max_length=100, null=True, blank=True)
    industry = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    web_url = models.URLField(null=True, blank=True)
    full_time_employees = models.IntegerField(null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='followed_stocks', 
        blank=True
    )
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"



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
        decimal_places=2,
        null=True,
        blank=True
    )
    forward_annual_dividend_yield = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        null=True,
        blank=True
    )
    payout_ratio = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True
    )
    dividend_date = models.DateField(null=True, blank=True)
    ex_dividend_date = models.DateField(null=True, blank=True)
    last_split_factor = models.CharField(null=True, blank=True, max_length=20)
    last_split_date = models.DateField(null=True, blank=True)

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
    dividends_paid = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
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
    total_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    gross_profit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    net_income = models.DecimalField(
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
    
    
class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notes')
    stock = models.ForeignKey(General, on_delete=models.CASCADE, related_name='stock_notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note by {self.user.username} on {self.stock.name}"
    

class StockPrices(models.Model):
    general = models.ForeignKey(
        General, 
        on_delete=models.CASCADE, 
        related_name='stock_prices'
    )
    Y1 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    Y2 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    Y3 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    Y4 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    Y5 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    Y6 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))])
    cagr_5_years = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return f"Stock Prices for {self.general.name} ({self.general.code})"
    
    class Meta:
        verbose_name_plural = "Stock Prices"
        
        
class DividendYieldData(models.Model):
    general = models.OneToOneField(
        General,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='dividend_yield_data'
    )
    yield_Y1 = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    yield_Y2 = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    yield_Y3 = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    yield_Y4 = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    yield_Y5 = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    cagr_5_years = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)

    def __str__(self):
        return f"Dividend Yield Data for {self.general.name}"

    class Meta:
        verbose_name_plural = "Dividend Yield Data"        