from rest_framework import serializers
from .models import General, Highlights, Valuation, Technicals, SplitsDividends, AnalystRatings, Description, IncomeStatement, CAGR, CashFlow, BalanceSheet, Note, StockPrices, DividendYieldData
from django.contrib.auth.models import User

class IncomeStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeStatement
        fields = '__all__'

class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlights
        fields = '__all__'

class ValuationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valuation
        fields = '__all__'

class TechnicalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technicals
        fields = '__all__'

class SplitsDividendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SplitsDividends
        fields = '__all__'

class AnalystRatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalystRatings
        fields = '__all__'

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'
        
class CagrSerializer(serializers.ModelSerializer):
    class Meta:
        model = CAGR
        fields = '__all__'
        
class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheet
        fields = '__all__'

class CashFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow
        fields = '__all__'
        

class StockPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrices
        fields = '__all__'

class DividendYieldDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DividendYieldData
        fields = '__all__'        

class GeneralSerializer(serializers.ModelSerializer):
    highlights = HighlightSerializer(read_only=True)
    valuation = ValuationSerializer(read_only=True)
    technicals = TechnicalsSerializer(read_only=True)
    splits_dividends = SplitsDividendsSerializer(read_only=True)
    analyst_ratings = AnalystRatingsSerializer(read_only=True)
    general_description = DescriptionSerializer(read_only=True)
    general_cagr = CagrSerializer(read_only=True)
    income_statements = IncomeStatementSerializer(many=True, read_only=True)
    balance_sheets = BalanceSheetSerializer(many=True, read_only=True)
    cash_flows = CashFlowSerializer(many=True, read_only=True)    
    stock_prices = StockPricesSerializer(many=True, read_only=True)
    dividend_yield_data = DividendYieldDataSerializer(read_only=True)    

    class Meta:
        model = General
        fields = '__all__'
        
        
class NoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Note 
        fields = ['id', 'user', 'stock', 'content', 'created_at', 'updated_at']
        
        
class StockSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = General
        fields = ('code', 'name', 'primary_ticker')
        
        
class DividendSerializer(serializers.Serializer):
    # Fields from the General model
    name = serializers.CharField()
    primary_ticker = serializers.CharField()
    country_iso = serializers.CharField()
    industry = serializers.CharField()
    exchange = serializers.CharField()
    currency_symbol = serializers.CharField()

    # Fields from the Highlights model
    market_capitalization = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        source='highlights.market_capitalization'
    )
    pe_ratio = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        source='highlights.pe_ratio'
    )
    dividend_yield = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        source='highlights.dividend_yield'
    )

    # Fields from the SplitsDividends model
    forward_annual_dividend_yield = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        source='splits_dividends.forward_annual_dividend_yield'
    )
    payout_ratio = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        source='splits_dividends.payout_ratio'
    )
    dividend_date = serializers.DateField(
        source='splits_dividends.dividend_date'
    )

    # Fields from the DividendYieldData model
    cagr_5_years = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        source='dividend_yield_data.cagr_5_years'
    )

    class Meta:
        model = General   


        
        
