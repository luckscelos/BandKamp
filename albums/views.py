from rest_framework.views import APIView
from .models import Album
from .serializers import AlbumSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics
from users.models import User
from django.shortcuts import get_object_or_404


class AlbumView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

    serializer_class = AlbumSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        album_obj = get_object_or_404(User, pk=user_id)

        albuns = Album.objects.filter(album=album_obj)

        return albuns

    def perform_create(self, serializer):
        user_id = self.kwargs["user_id"]
        album_obj = get_object_or_404(User, pk=user_id)
        self.check_object_permissions(self.request, album_obj)
        return serializer.save(user_id=self.request.user.id)


class AlbumDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

    serializer_class = AlbumSerializer
    queryset = Album.objects.all()

    lookup_url_kwarg = "album_id"
