

from rest_framework import generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import  DjangoFilterBackend

from comment.serializers import CommentSerializer
from like.models import Favorite
from like.serializers import LikeUserSerializer
from post import serializers
from post.models import Post
from post.permissions import IsOwner, IsOwnerOrAdmin



class StandartResultPagination(PageNumberPagination):
    page_size = 4
    page_query_param = 'pages'


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_filter = ('title', 'body')
    filterset_fields = ('owner', 'category')



    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in('create', 'update', 'partial_update'):
            return serializers.PostCreateUpdateSerializer
        else:
            return serializers.PostDetailSerializer




    def get_permissions(self):

    # удалять может только автор поста или админ
        if self.action == 'destroy':
            return [IsOwnerOrAdmin(),]
    # обнавлять может только автор поста
        elif self.action in ('update', 'partial_apdate'):
            return [IsOwner(),]
    # просматривать могулт все (list, retrieve)
    # на создавать может залогиненный пользователь
        return [permissions.IsAuthenticatedOrReadOnly(),]


    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status=200)


    @action(['GET'], detail=True)
    def likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeUserSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        post = self.get_object()
        user = request.user
        favorite = user.favorites.filter(post=post)

        if request.method == 'POST':
            if favorite.exists():
                return Response({'msg': 'Already in Favorites'}, status=400)
            Favorite.objects.create(owner=user, post=post)
            return Response({'msg': 'Added to Favorite'}, status=201)

        if favorite.exists():
            favorite.delete()
            return Response({'msg': 'Deleted from Favorites'}, status=204)
        return Response({'msg': 'Favorite Not Found!'}, status=404)








class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PostListSerializer
        return serializers.PostCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)





class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return serializers.PostCreateUpdateSerializer
        return serializers.PostDetailSerializer


    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [IsOwner()]
        elif self.request.method == 'DELETE':
            return [IsOwnerOrAdmin()]
        return [permissions.AllowAny()]
