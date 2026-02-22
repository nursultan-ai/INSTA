from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User  # Убедись, что здесь именно переменная User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar', 'is_official']  # Выбираем главные поля


class PostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostContent
        fields = ['id', 'file']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Чтобы видели имя, а не ID

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_date']


class PostSerializer(serializers.ModelSerializer):
    # ИСПРАВЛЕНИЕ: используем related_name='contents' из модели, а не postcontent_set
    contents = PostContentSerializer(many=True, read_only=True)

    # ДОБАВЛЕНИЕ: чтобы в DETAIL сразу видеть комменты и их количество
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    author = UserProfileSerializer(read_only=True)  # Чтобы видеть инфо об авторе

    class Meta:
        model = Post
        fields = ['id', 'author', 'description', 'hashtags', 'music',
                  'contents', 'comments', 'likes_count', 'created_date']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'