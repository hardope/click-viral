# Description: View for deleting posts and comments
from django.http import HttpResponse
from ..models import Post, Comment

root = "/home/clickviral/clickviral"
# Create your views here.

def delete(request, query):
    try:
        post = Post.objects.get(id=query)
    except:
        post = Comment.objects.get(id=query)

    if post.to_dict(request.user.id)["name"] == request.user.username:
        pass
    else:
        return HttpResponse("...")

    if post.media != "empty":
        try:
            os.remove(f"{root}/media/posts/{post.id}.{post.media}")
        except:
            pass
    else:
        pass

    try:
        post = Post.objects.get(id=query).delete()
    except:
        post = Comment.objects.get(id=query).delete()
    return HttpResponse("...")