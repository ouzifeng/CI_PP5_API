from django.db.models import Q
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import General, Note
from .serializers import (
    GeneralSerializer, NoteSerializer, StockSearchSerializer,
    DividendSerializer
)
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination


class StockDetailView(generics.RetrieveAPIView):
    queryset = General.objects.all()
    serializer_class = GeneralSerializer
    lookup_field = 'uid'

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
            'cash_flows',
            'stock_prices',
            'dividend_yield_data'
        ).select_related('prices').all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if request.user.is_authenticated:
            user = request.user
            is_following = instance.followers.filter(id=user.id).exists()
        else:
            is_following = False

        data = serializer.data
        data['is_following'] = is_following

        return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow_stock(request, uid):
    try:
        stock = General.objects.get(uid=uid)
    except General.DoesNotExist:
        return Response(
            {"error": "Stock not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    user = request.user

    if stock.followers.filter(id=user.id).exists():
        # User is already following the stock, so unfollow
        stock.followers.remove(user)
        action = 'unfollowed'
    else:
        # User is not following the stock, so follow
        stock.followers.add(user)
        action = 'followed'

    return Response({"status": "ok", "action": action})


class NoteListCreate(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print("Received data for new note:", serializer.validated_data)
        serializer.save(user=self.request.user)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class FollowedStocksView(generics.ListAPIView):
    serializer_class = GeneralSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return General.objects.filter(followers=user)


class FollowedStocksList(generics.ListAPIView):
    serializer_class = GeneralSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return General.objects.filter(followers=user)


class StockSearchView(generics.ListAPIView):
    serializer_class = StockSearchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = General.objects.all()
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(
                Q(code__icontains=query) | Q(name__icontains=query)
            )
        return queryset


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class DividendDataListView(generics.ListAPIView):
    serializer_class = DividendSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        min_yield = self.request.query_params.get('min_dividend_yield')
        max_yield = self.request.query_params.get('max_dividend_yield')
        min_payout = self.request.query_params.get('min_payout_ratio')
        max_payout = self.request.query_params.get('max_payout_ratio')
        min_pe = self.request.query_params.get('min_pe_ratio')
        max_pe = self.request.query_params.get('max_pe_ratio')

        queryset = General.objects.all()
        if min_yield and max_yield:
            queryset = queryset.filter(
                highlights__dividend_yield__gte=float(min_yield),
                highlights__dividend_yield__lte=float(max_yield)
            )
        if min_payout and max_payout:
            queryset = queryset.filter(
                splits_dividends__payout_ratio__gte=float(min_payout),
                splits_dividends__payout_ratio__lte=float(max_payout)
            )
        if min_pe and max_pe:
            queryset = queryset.filter(
                highlights__pe_ratio__gte=float(min_pe),
                highlights__pe_ratio__lte=float(max_pe)
            )

        return queryset
