from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth.models import User
from main.parse_time import get_time
import sys

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=1000, default="")
    image = models.CharField(max_length=50, default="empty")
    gender = models.CharField(max_length=20, default="Null")
    visibility = models.CharField(max_length=20, default="visible")
    followers = models.IntegerField(default=0)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
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

        return {"id": str(self.id),
                "name": self.user,
                "article": self.article,
                "media": self.media,
                "likes": count_like(self.id),
                "like_value": like_value,
                "created_at": f"{get_time(self.created_at)}",
                "comments": self.comments,
                "edited": self.edited,
                "edited_at": f"{get_time(self.created_at)}",
                }

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null=True)
    m_comment = models.ForeignKey('self', on_delete = models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
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

        return {"id": str(self.id),
                "post": str(self.post_id),
                "name": self.user,
                "article": self.article,
                "media": self.media,
                "likes": count_like(self.id),
                "like_value": like_value,
                "created_at": f"{get_time(self.created_at)}",
                "comments": self.comments,
                "edited": self.edited,
                "edited_at": f"{get_time(self.created_at)}",
                }

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    time = models.DateTimeField(default=datetime.now)

    def name_user(self):
        return User.objects.get(id=self.user_id).username

def count_like(id):
    count = 0

    try:
        post = Post.objects.get(id=id)
        sys.stderr.write("Found post\n\n")
        count+=len([Like.objects.filter(post_id=id)])-1
        sys.stderr.write(count + "\n\n")
        post.likes = count
        post.save()
    except:
        comment = Comment.objects.get(id=id)
        count += len([Like.objects.filter(comment_id=id)])-1
        comment.likes = count
        comment.save()
    
    sys.stderr.write(count + '\n\n')
    return count





