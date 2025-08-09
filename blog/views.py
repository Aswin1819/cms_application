from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import BlogPost, Comment, ReadLog
from .serializers import BlogPostSerializers, BlogPostDetailSerializer, CommentSerializer

class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(status='published')
    serializer_class = BlogPostSerializers
    permission_classes = [IsAuthenticated]


class BlogPostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        post = get_object_or_404(BlogPost, slug=slug, status='published')
        
        # Track read count for logged-in users
        if request.user.is_authenticated:
            if not ReadLog.objects.filter(post=post, user=request.user).exists():
                ReadLog.objects.create(post=post, user=request.user)
                post.read_count += 1
                post.save()

        serializer = BlogPostDetailSerializer(post)
        return Response(serializer.data)



class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        post = get_object_or_404(BlogPost, pk=post_id, status='published')
        serializer.save(user=self.request.user, post=post)


class BlogPostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        
        post = get_object_or_404(BlogPost, pk=pk, status='published')
        user = request.user
        
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
            post.dislikes.remove(user)
            
        return Response({
            "likes_count": post.likes.count(),
            "dislikes_count": post.dislikes.count()
        }, status=status.HTTP_200_OK)
        

class BlogPostDislikeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, pk=pk, status='published')
        user = request.user
        
        if user in post.dislikes.all():
            post.dislikes.remove(user)
        else:
            post.dislikes.add(user)
            post.likes.remove(user)
        return Response({
            "likes_count":post.likes.count(),
            "dislikes_count":post.dislikes.count()
        },status=status.HTTP_200_OK)
        
