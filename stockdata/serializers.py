from rest_framework import serializers
from .models import General, Highlights, Valuation, Technicals, SplitsDividends, AnalystRatings, Description, IncomeStatement, CAGR, CashFlow, BalanceSheet

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

    class Meta:
        model = General
        fields = '__all__'

        
        
