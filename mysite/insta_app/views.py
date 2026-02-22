from rest_framework import viewsets, permissions, filters
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAuthorOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception:
            return Response(status=400)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'hashtags__hashtag_name']
    search_fields = ['description', 'author__username']
    ordering_fields = ['created_date']
    ordering = ['-created_date']

    def get_queryset(self):
        return Post.objects.select_related('author').prefetch_related(
            'contents', 'hashtags', 'comments__user', 'likes'
        ).all().order_by('-created_date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.select_related('user', 'post').all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Follow.objects.select_related('follower', 'following').all()

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

class PostLikeViewSet(viewsets.ModelViewSet):
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return PostLike.objects.select_related('user', 'post').all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentLikeViewSet(viewsets.ModelViewSet):
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return CommentLike.objects.select_related('user', 'comment').all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteItemViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteItem.objects.filter(favorite__user=self.request.user).select_related('post')

class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer

class PostContentViewSet(viewsets.ModelViewSet):
    queryset = PostContent.objects.select_related('post').all()
    serializer_class = PostContentSerializer