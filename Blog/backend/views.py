from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework import status
from .models import *
from backend.serializers import *
from rest_framework import serializers, viewsets
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework.pagination import LimitOffsetPagination
from django.http import HttpResponse, HttpRequest
from django.conf import settings as django_settings
from django.db.models import F


class AdminBlogView(APIView):
	#get blog for admin
	@method_decorator(login_required)				
	def get (self, request, format=None) :
		try:
			user = User.objects.get(username=request.user)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		if not user.is_staff:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		try:
			blog = Blog.objects.all()
		except Blog.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		serializer = AdminBlogSerializer(blog, context={'request': request}, many=True,)		
		return Response(serializer.data)

	@method_decorator(login_required)				
	def post (self, request, format=None) :
		try:
			user = User.objects.get(username=request.user)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		if not user.is_staff:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		users = []
		users.append(user.pk)
		request.data['users'] = users
		serializer = AdminBlogSerializer(data = request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
class BlogView(APIView):

	@method_decorator(login_required)				
	def get (self, request, format=None) :
		try:
			user = User.objects.get(username=request.user)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		try:
			blog = Blog.objects.all()
		except Blog.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		serializer = BlogSerializer(blog, context={'request': request}, many=True,)		
		return Response(serializer.data)

class BlogUsersView(APIView):
	@method_decorator(login_required)				
	def get (self, request,pk, format=None) :
		try:
			user = User.objects.get(username=request.user)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		if not user.is_staff:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		try:
			users = User.objects.filter(blog = pk)
		except User.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = UserSerializer(users, context={'request': request}, many=True,)

		return Response(serializer.data)

class BlogPostView(APIView):
	@method_decorator(login_required)				
	def get (self, request,pk, format=None) :
		try:
			user = User.objects.get(username=request.user)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		if not user.is_staff:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		try:
			posts = Post.objects.filter(blog = pk)
		except Post.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = PostSerializer(posts, context={'request': request}, many=True,)

		return Response(serializer.data)

class UserPostView(APIView):
	@method_decorator(login_required)				
	def get (self, request,pk, format=None) :
		try:
			user = User.objects.get(username=request.user)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		if not user.is_staff:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		try:
			posts = Post.objects.filter(user = pk)
		except Post.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = PostSerializer(posts, context={'request': request}, many=True,)

		return Response(serializer.data)

class RegisterUserToBlogView(APIView):
	@method_decorator(login_required)				
	def post (self, request, format=None) :

		try:
			user = User.objects.get(username=request.user)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		
		blog_id = request.data['blog']

		try:
			blog = Blog.objects.get(pk = blog_id)
		except Blog.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		blog.users.add(user)
		blog.save()
		return Response(status=status.HTTP_200_OK)

class PostView(APIView):
	@method_decorator(login_required)				
	def get (self, request,pk=None, format=None) :
		try:
			user = User.objects.get(username=request.user)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		try:
			posts = Post.objects.filter(blog = pk)
		except Post.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer = PostSerializer(posts, context={'request': request}, many=True,)

		return Response(serializer.data)


	@method_decorator(login_required)				
	def post (self, request, format=None) :

		blog_id = request.data['blog']
		try:
			user = User.objects.get(username=request.user,blog = blog_id)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		
		request.data['user'] = user.pk
		serializer = PostSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(login_required)				
	def put (self, request,pk, format=None) :

		
		try:
			user = User.objects.get(username=request.user,post = pk)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		try:
			post = Post.objects.get(pk = pk)

		except Post.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		request.data['user'] = user.pk
		request.data['blog'] = post.blog.pk
		serializer = PostSerializer(post,data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(login_required)				
	def delete (self, request,pk, format=None) :

		
		try:
			user = User.objects.get(username=request.user,post = pk)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		try:
			post = Post.objects.get(pk = pk)

		except Post.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		post.delete()
		
		return Response(status=status.HTTP_200_OK)

class CommentView(APIView):
	@method_decorator(login_required)				
	def get (self, request,pk=None, format=None) :
		try:
			user = User.objects.get(username=request.user)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		
		comments = Comment.objects.filter(post = pk)
		serializer = CommentSerializer(comments, context={'request': request}, many=True,)
		return Response(serializer.data)


	@method_decorator(login_required)				
	def post (self, request, format=None) :
		post_id = request.data['post']
		blog = Blog.objects.get(post = post_id)
		try:
			user = User.objects.get(username=request.user,blog = blog)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		request.data['user'] = user.pk
		serializer = CommentSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(login_required)				
	def put (self, request,pk, format=None) :

		try:
			user = User.objects.get(username=request.user,comment = pk)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		try:
			comment = Comment.objects.get(pk = pk)

		except Comment.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		request.data['user'] = user.pk
		request.data['post'] = comment.post.pk
		serializer = CommentSerializer(comment,data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@method_decorator(login_required)				
	def delete (self, request,pk, format=None) :

		try:
			user = User.objects.get(username=request.user,comment = pk)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		try:
			comment = Comment.objects.get(pk = pk)

		except Comment.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		
		comment.delete()
		
		return Response(status=status.HTTP_200_OK)

class GetCommentsForUSerView(APIView):
	@method_decorator(login_required)				
	def get (self, request,pk, format=None) :
		try:
			user = User.objects.get(username=request.user)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		if not user.is_staff:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		comments = Comment.objects.filter(user = pk)

		serializer = AdminCommentSerializer(comments, context={'request': request}, many=True,)

		return Response(serializer.data)

class LikePostView(APIView):
	@method_decorator(login_required)				
	def post (self, request, format=None) :
		post_id = request.data['post']
		blog = Blog.objects.get(post = post_id)
		try:
			user = User.objects.get(username=request.user,blog = blog)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		Post.objects.filter(pk = post_id).update(total_likes = F('total_likes')+1)
		return Response(status=status.HTTP_200_OK)

class LikeCommentView(APIView):
	@method_decorator(login_required)				
	def post (self, request, format=None) :
		comment_id = request.data['comment']
		comment = Comment.objects.get(pk = comment_id)
		try:
			user = User.objects.get(username=request.user,blog = comment.post.blog)
		except User.DoesNotExist:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		comment.total_likes += 1
		comment.save()
		return Response(status=status.HTTP_200_OK)


		




