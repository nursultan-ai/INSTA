from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='users')
router.register(r'follows', FollowViewSet, basename='follows')
router.register(r'hashtags', HashtagViewSet, basename='hashtags')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'post-contents', PostContentViewSet, basename='post-contents')
router.register(r'post-likes', PostLikeViewSet, basename='post-likes')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'comment-likes', CommentLikeViewSet, basename='comment-likes')
router.register(r'favorites', FavoriteViewSet, basename='favorites')
router.register(r'favorite-items', FavoriteItemViewSet, basename='favorite-items')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]