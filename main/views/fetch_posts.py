from .models import Post, Like, Comment, Follow, Otp, Profile, Chat
from django.db.models import Q
from django.contrib.auth.models import User
from collections import deque
import random
from django.db.models import Count


def collect_personalized_posts(current_user):
    following_posts = list(get_posts_authored_by_following_users(current_user))
    liked_commented_posts = list(get_posts_liked_or_commented_by_user(current_user))
    chat_posts = list(get_posts_by_chatted_users(current_user))
    average_interactions = calculate_average_interactions()
    viral_posts = list(get_viral_posts(average_interactions))
    user_posts = list(get_current_user_posts(current_user))
    random_posts = list(get_random_posts())

    combined_posts = list(
        set(
            following_posts
            + liked_commented_posts
            + chat_posts
            + viral_posts
            + user_posts
            + random_posts
        )
    )
    sorted_posts = sort_posts_by_interactions(combined_posts, current_user)
    return sorted_posts


def get_posts_by_chatted_users(current_user):
    chatted_users = Chat.objects.filter(sender=current_user).values_list(
        "recipient", flat=True
    )
    chatted_posts = Post.objects.filter(user__in=chatted_users)
    return chatted_posts


def get_posts_authored_by_following_users(current_user):
    following_users = Follow.objects.filter(user=current_user).values_list(
        "follow", flat=True
    )
    return Post.objects.filter(user__in=following_users)


def get_posts_liked_or_commented_by_user(current_user):
    liked_posts = Like.objects.filter(
        user=current_user, post__isnull=False
    ).values_list("post", flat=True)
    commented_posts = Like.objects.filter(
        user=current_user, comment__isnull=False
    ).values_list("comment__post", flat=True)
    return Post.objects.filter(id__in=list(liked_posts) + list(commented_posts))


def calculate_average_interactions():
    average_interactions = Post.objects.aggregate(
        avg_interactions=Count("likes") + Count("comment")
    )["avg_interactions"]
    return average_interactions


def get_viral_posts(average_interactions):
    return Post.objects.annotate(
        total_interactions=Count("likes") + Count("comment")
    ).filter(total_interactions__gt=average_interactions)


def get_current_user_posts(current_user):
    return Post.objects.filter(user=current_user)


def get_random_posts():
    all_posts = list(Post.objects.all())
    random.shuffle(all_posts)
    random_posts = all_posts[:5]  # Adjust the number of random posts as needed
    return random_posts


def sort_posts_by_interactions(posts, current_user):
    sorting_option = random.choice(["time", "interactions", "user_interactions"])

    if sorting_option == "time":
        sorted_posts = sorted(posts, key=lambda post: post.created_at, reverse=True)
    elif sorting_option == "interactions":
        sorted_posts = sorted(
            posts, key=lambda post: post.likes + post.comments, reverse=True
        )
    else:  # sorting_option == 'user_interactions'
        sorted_posts = sorted(
            posts,
            key=lambda post: calculate_user_interactions(current_user, post),
            reverse=True,
        )

    return sorted_posts


def calculate_user_interactions(user, post):
    return (
        Like.objects.filter(user=user, post=post).count()
        + Like.objects.filter(user=post.user, post=post).count()
    )
