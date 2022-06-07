from rest_framework import generics, permissions
from . import serializers
from .models import Rating
from rest_framework.views import APIView
from .parsing import get_info, get_html, BASE_URL
from rest_framework.response import Response


class RatingCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.RatingSerializer
    permissions = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ParsingView(APIView):

    def get(self, request):
        parsing = get_info(get_html(BASE_URL))
        return Response(parsing)