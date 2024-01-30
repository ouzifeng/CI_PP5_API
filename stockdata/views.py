from django.shortcuts import render
from rest_framework import generics
from .models import General
from .serializers import GeneralSerializer, HighlightSerializer, ValuationSerializer, TechnicalsSerializer, SplitsDividendsSerializer, AnalystRatingsSerializer, DescriptionSerializer, IncomeStatementSerializer, CagrSerializer

class StockDetailView(generics.RetrieveAPIView):
    queryset = General.objects.all()
    serializer_class = GeneralSerializer
    lookup_field = 'primary_ticker'

    def get_queryset(self):
        return General.objects.prefetch_related(
            'highlights',
            'valuation',
            'technicals',
            'splits_dividends',
            'analyst_ratings',
            'general_description',
            'general_cagr',
            'income_statements',
            'balance_sheets',
            'cash_flows'
        ).all()

