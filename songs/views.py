from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Song
from albums.models import Album
from rest_framework import generics


class SongView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Song.objects.all()

        return Song.objects.all(owner=self.request.user)

    def get_queryset_(self):
        album_id = self.kwargs["album_id"]
        song_obj = get_object_or_404(Album, pk=album_id)

        songs = Album.objects.filter(song=song_obj)

        return songs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
