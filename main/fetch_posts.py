from .models import Post, Like, Comment, Follow, Otp, Profile, Chat
from django.db.models import Q
from django.contrib.auth.models import User

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
    user_graph = build_user_graph(user)

    # Step 2: Perform iterative graph traversal (depth-first search) to collect posts
    posts = []
    stack = [user_graph]
    visited = set()

    while stack:
        node = stack.pop()
        if node.user not in visited:
            visited.add(node.user)
            posts.extend(Post.objects.filter(user_id=node.user).order_by('-created_at'))

            for next_user in node.next_users:
                stack.append(next_user)

    return posts