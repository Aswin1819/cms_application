from django.urls import path
from .views import *


urlpatterns = [
    #blog management
    path('blogs/',AdminBlogPostListCreateView.as_view(), name='admin-blog-list-create'),
    path('blogs/<int:pk>/',AdminBlogPostRetrieveUpdateDeleteView.as_view(), name='admin-blog-detail'),
    
    #user management
    path('users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('users/<int:pk>/delete/',AdminUserDeleteView.as_view(), name='admin-user-delete'),
    
    #comment moderation
    path('comments/', AdminCommentListView.as_view(), name='admin-comment-list'),
    path('comments/<int:pk>/approve/', AdminCommentApproveView.as_view(), name='admin-comment-approve'),
    
    
]
