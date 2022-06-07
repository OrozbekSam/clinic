from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from account.permissions import IsAdminOrReadOnly
from . import serializers
from doctor.models import Doctor, Medicine, Comment, Likes, Favorite

User = get_user_model()


class StandartPaginationClass(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    pagination_class = StandartPaginationClass
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('gender', 'experience_year', 'category')
    search_fields = ['first_name', 'last_name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.DoctorListSerializer
        else:
            return serializers.DoctorSerializer

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        doctor = self.get_object()
        comments = doctor.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(['POST'], detail=True)
    def add_to_liked(self, request, pk):
        doctor = self.get_object()
        if request.user.liked.filter(doctor=doctor).exists():
            return Response('You already like it!', status=status.HTTP_400_BAD_REQUEST)
        Likes.objects.create(doctor=doctor, user=request.user)
        return Response('You like it!', status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def remove_from_liked(self, request, pk):
        doctor = self.get_object()
        if not request.user.liked.filter(doctor=doctor).exists():
            return Response('You didn"t like it!', status=status.HTTP_400_BAD_REQUEST)
        request.user.liked.filter(doctor=doctor).delete()
        return Response('Your like removed!', status=status.HTTP_204_NO_CONTENT)

    @action(['POST'], detail=True)
    def add_to_favorites(self, request, pk):
        doctor = self.get_object()
        if request.user.favorites.filter(doctor=doctor).exists():
            return Response('You have already added this master to favorites', status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(doctor=doctor, user=request.user)
        return Response('You added it to favorites', status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def remove_from_favorites(self, request, pk):
        doctor = self.get_object()
        if not request.user.favorites.filter(doctor=doctor).exists():
            return Response("You haven't added it to favorites", status=status.HTTP_400_BAD_REQUEST)
        request.user.favorites.filter(doctor=doctor, ).delete()
        return Response('The doctor is removed from favorites', status=status.HTTP_204_NO_CONTENT)


class MedicineViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = serializers.MedicineSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = StandartPaginationClass
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('type',)
    search_fields = ('type',)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    class Meta:
        model = Comment
        exclude = 'comments_detail'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserFavoriteList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        user = request.user
        doctor = user.favorites.all()
        serializer = serializers.FavoriteSerializer(doctor, many=True).data
        return Response(serializer)