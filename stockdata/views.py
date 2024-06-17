from django.db.models import Q
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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

    @swagger_auto_schema(
        operation_description="Retrieve details of a stock",
        responses={200: GeneralSerializer}
    )
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


@swagger_auto_schema(
    method='post',
    operation_description="Toggle follow/unfollow a stock",
    responses={200: openapi.Response('Successful operation', openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'action': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ))}
)
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

    @swagger_auto_schema(
        operation_description="List and create notes",
        responses={200: NoteSerializer(many=True)},
        request_body=NoteSerializer
    )
    def perform_create(self, serializer):
        print("Received data for new note:", serializer.validated_data)
        serializer.save(user=self.request.user)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a note",
        responses={200: NoteSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a note",
        request_body=NoteSerializer,
        responses={200: NoteSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a note",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class FollowedStocksView(generics.ListAPIView):
    serializer_class = GeneralSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all stocks followed by the user",
        responses={200: GeneralSerializer(many=True)}
    )
    def get_queryset(self):
        user = self.request.user
        return General.objects.filter(followers=user)


class StockSearchView(generics.ListAPIView):
    serializer_class = StockSearchSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Search stocks by code or name",
        manual_parameters=[
            openapi.Parameter(
                'query', openapi.IN_QUERY, description="Search query",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: StockSearchSerializer(many=True)}
    )
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

    @swagger_auto_schema(
        operation_description="List dividend data with filters",
        manual_parameters=[
            openapi.Parameter(
                'min_dividend_yield',
                openapi.IN_QUERY,
                description="Minimum dividend yield",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_dividend_yield',
                openapi.IN_QUERY,
                description="Maximum dividend yield",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'min_payout_ratio',
                openapi.IN_QUERY,
                description="Minimum payout ratio",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_payout_ratio',
                openapi.IN_QUERY,
                description="Maximum payout ratio",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'min_pe_ratio',
                openapi.IN_QUERY,
                description="Minimum P/E ratio",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_pe_ratio',
                openapi.IN_QUERY,
                description="Maximum P/E ratio",
                type=openapi.TYPE_NUMBER
            ),
        ],
        responses={200: DividendSerializer(many=True)}
    )
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

        queryset = queryset.order_by('-highlights__dividend_yield')

        return queryset
