from rest_framework.views import APIView
from .models import Album
from .serializers import AlbumSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class AlbumView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    albums = Album.objects.all()

    serializer_class = AlbumSerializer()

    def perform_create(self, serializer):
        return serializer.save(user_id=self.request.user.id)
