from .models import Post, Like, Comment, Follow, Otp, Profile, Chat
from django.db.models import Q
from django.contrib.auth.models import User
from collections import

class UserNode:
    def __init__(self, user):
        self.user = user
        self.next_users = []

def build_user_graph(user):
    # Step 1: Retrieve the user's followers
    followers = Follow.objects.filter(user=user).values_list('follow_id', flat=True)

    # Step 2: Retrieve the posts liked by the user
    liked_posts = Like.objects.filter(user=user, post__isnull=False).values_list('post__user_id', flat=True)

    # Step 3: Retrieve the users the current user has chatted with
    chat_users = Chat.objects.filter(Q(sender=user) | Q(recipient=user)).values_list('sender_id', 'recipient_id')
    chat_users = set(sum(chat_users, ()))  # Combine sender and recipient IDs

    # Step 4: Combine the lists of followers, liked user IDs, and chat users
    user_ids = set(followers) | set(liked_posts) | chat_users

    # Step 5: Build the user graph
    user_nodes = {}
    for uid in user_ids:
        user_nodes[uid] = UserNode(uid)

    # Step 6: Connect the user nodes
    for uid, node in user_nodes.items():
        if uid in followers:
            node.next_users.extend([user_nodes[follow_id] for follow_id in followers])

        if uid in liked_posts:
            node.next_users.append(user_nodes[uid])

        if uid in chat_users:
            node.next_users.append(user_nodes[uid])

    return user_nodes[user.id]

def get_posts(user):
    # Step 1: Build the user graph
    user_graph = build_user_graph(user)

    # Step 2: Perform iterative graph traversal (breadth-first search) to collect posts
    posts = []
    visited = set()
    queue = deque([(user_graph, None)])  # Tuple of (node, parent_post_id)

    while queue:
        node, parent_post_id = queue.popleft()

        if node.user not in visited:
            visited.add(node.user)

            # Retrieve posts from the current user
            if parent_post_id is None:
                posts.extend(Post.objects.filter(user_id=node.user).order_by('-created_at'))

            # Retrieve posts from followed users
            if parent_post_id is not None:
                posts.extend(Post.objects.filter(user_id=node.user, id=parent_post_id).order_by('-created_at'))

            # Retrieve posts from users whose posts have been liked by the current user
            liked_posts = Like.objects.filter(user=user, post__user_id=node.user).values_list('post_id', flat=True)
            posts.extend(Post.objects.filter(user_id=node.user, id__in=liked_posts).order_by('-created_at'))

            # Retrieve posts from authors of posts commented on by the current user
            commented_posts = Comment.objects.filter(user=user, post__user__id=node.user).values_list('post_id', flat=True)
            posts.extend(Post.objects.filter(id__in=commented_posts).order_by('-created_at'))

            # Retrieve comments from the current user's posts
            comments = Comment.objects.filter(user_id=node.user, post_id=parent_post_id).order_by('created_at')
            posts.extend(comments)

            # Traverse to the next user nodes
            for next_user in node.next_users:
                queue.append((next_user, parent_post_id))
