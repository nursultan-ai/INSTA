from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    birth_day = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('undefined', 'Undefined'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='undefined')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    url_link = models.URLField(null=True, blank=True)
    is_official = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    date_registered = models.DateField(auto_now_add=True)

    def str(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=100, unique=True)

    def str(self):
        return f"#{self.hashtag_name}"

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField(null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    music = models.FileField(upload_to='music/', null=True, blank=True)
    tagged_users = models.ManyToManyField(UserProfile, blank=True, related_name='tagged_in_posts')
    created_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.author.username} - {self.created_date}"

class PostContent(models.Model):
    post = models.ForeignKey(Post, related_name='contents', on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_contents/') # Сүрөт же Видео үчүн

class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.username}: {self.text[:20]}"

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='favorite_folder')

class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, related_name='items', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)