from django.urls import path
from . views import *



urlpatterns = [
    path('',BlogPostListView.as_view(), name='blog-list'),
    path('<slug:slug>/',BlogPostDetailView.as_view(), name='blog-detail'),
    path('<int:pk>/like/', BlogPostLikeView.as_view(), name='blog-like'),
    path('<int:pk>/dislike/',BlogPostDislikeView.as_view(), name='blog-dislike'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='comment-create'),
]

