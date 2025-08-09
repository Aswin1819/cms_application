# adminapp/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from blog.models import BlogPost, Comment
from authentication.models import CustomUser
from .serializers import AdminBlogPostSerializer, AdminUserSerializer, AdminCommentSerializer
from .permissions import IsAdminUserJWT

# Blog CRUD
class AdminBlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = AdminBlogPostSerializer
    permission_classes = [IsAuthenticated, IsAdminUserJWT]

class AdminBlogPostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = AdminBlogPostSerializer
    permission_classes = [IsAuthenticated, IsAdminUserJWT]

# User Management
class AdminUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserJWT]

class AdminUserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserJWT]

# Comment Moderation
class AdminCommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = AdminCommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUserJWT]

class AdminCommentApproveView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = AdminCommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUserJWT]

    def patch(self, request, *args, **kwargs):
        comment = self.get_object()
        
        was_approved = comment.is_approved
        comment.is_approved = not was_approved
        comment.save()

        serializer = self.get_serializer(comment)
        
        message = "comment approved" if not was_approved else "comment rejected"
        return Response(
            {
                "message": message,
                "comment": serializer.data
            },
            status=status.HTTP_200_OK
        )
