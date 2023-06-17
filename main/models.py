from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth.models import User
from main.parse_time import get_time
import sys

# Create your models here.


class Otp(models.Model):
    mail = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    otp = models.CharField(max_length=7)
    tries = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.username} - {self.mail}"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=1000, default="")
    image = models.CharField(max_length=50, default="empty")
    gender = models.CharField(max_length=20, default="Null")
    location = models.CharField(max_length=20, default="Null")
    birthday = models.CharField(max_length=100, default="Null")
    followers = models.IntegerField(default=0)
    birthyear = models.CharField(max_length=5, default="")

    def __str__(self):
        return f"{self.user.username}"


class Preference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.BooleanField(default=True)
    location = models.BooleanField(default=True)
    gender = models.BooleanField(default=True)
    birthday = models.BooleanField(default=True)
    birthyear = models.BooleanField(default=False)
    login_verification = models.BooleanField(default=False)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return f"{self.follow.username} - {self.user.username}"


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.TextField(default="")
    media = models.CharField(max_length=100, default="empty")
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    edited_at = models.DateTimeField(default=datetime.now)

    def to_dict(self, user):
        try:
            count_likes = Like.objects.get(user_id=user, post_id=self.id)
            like_value = "True"
        except:
            like_value = "False"

        return {
            "id": str(self.id),
            "name": self.user.username,
            "article": parse_post(self.article),
            "raw_article": self.article,
            "media": self.media,
            "likes": count_like(self.id),
            "like_value": like_value,
            "created_at": f"{get_time(self.created_at)}",
            "comments": count_comments(self.id),
            "edited": self.edited,
            "edited_at": f"{get_time(self.created_at)}",
        }

    def __str__(self):
        return f"{self.user.username} - {self.id}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    m_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.TextField(default="")
    media = models.CharField(max_length=100, default="empty")
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    edited_at = models.DateTimeField(default=datetime.now)

    def to_dict(self, user):
        try:
            try:
                count_likes = Like.objects.get(user_id=user, post_id=self.id)
            except:
                count_likes = Like.objects.get(user_id=user, comment_id=self.id)
            like_value = "True"
        except:
            like_value = "False"

        return {
            "id": str(self.id),
            "post": str(self.post_id),
            "name": self.user.username,
            "article": parse_post(self.article),
            "raw_article": self.article,
            "media": self.media,
            "likes": count_like(self.id),
            "like_value": like_value,
            "created_at": f"{get_time(self.created_at)}",
            "comments": count_comments(self.id),
            "edited": self.edited,
            "edited_at": f"{get_time(self.created_at)}",
        }

    def __str__(self):
        return f"{self.user.username} - {self.id}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=datetime.now)

    def name_user(self):
        return User.objects.get(id=self.user_id).username


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipient"
    )
    message = models.TextField(default="")
    media = models.CharField(max_length=10, default="empty")
    created_at = models.DateTimeField(default=datetime.now)

    def to_dict(self):
        return {
            "id": str(self.id),
            "sender": self.sender.username,
            "recipient": self.recipient.username,
            "message": self.message,
            "media": self.media,
            "created_at": f"{get_time(self.created_at)}",
        }

    def __str__(self):
        return f"{self.sender.username} - {self.recipient.username}"


def count_like(id):
    count = 0

    try:
        post = Post.objects.get(id=id)
        likes = Like.objects.filter(post_id=id)
        count = count_objects(likes)
        post.likes = count
        post.save()
    except:
        comment = Comment.objects.get(id=id)
        likes = Like.objects.filter(comment_id=id)
        count = count_objects(likes)
        comment.save()

    return count


def count_comments(id):
    count = 0
    try:
        post = Post.objects.get(id=id)
        comments = Comment.objects.filter(post_id=id)
        count = count_objects(comments)
        post.comments = count
        post.save()
    except:
        comment = Comment.objects.get(id=id)
        comments = Comment.objects.filter(m_comment_id=id)
        count = count_objects(comments)
        comment.comments = count
        comment.save()
    return count


def count_objects(model):
    return len([str(i) for i in model])


def parse_post(article):
    parsed = []
    paragraphs = article.split("\n")
    for i in paragraphs:
        if i == "":
            paragraphs.remove(i)
        else:
            parsed.append({"tag": "p", "text": i})
    return parsed
