from django.contrib import admin
from .models import (UserProfile, Follow, Hashtag, Post,
                     PostContent, PostLike, Comment,
                     CommentLike, Favorite, FavoriteItem)


class PostContentInline(admin.TabularInline):
    model = PostContent
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_date', 'description_short')
    search_fields = ('author__username', 'description')
    list_filter = ('created_date',)
    inlines = [PostContentInline, CommentInline]

    def description_short(self, obj):
        return obj.description[:50] if obj.description else ""

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'gender', 'is_official', 'date_registered')
    list_editable = ('is_official',)
    search_fields = ('username', 'phone_number')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_date')


admin.site.register(Hashtag)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)