from django.contrib.auth.models import User
from rest_framework import  serializers
from backend.models import *

# Serializers define the API representation.
class AdminBlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username','email')

class BlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields = ('title','description')

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'

class AdminCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('post','content','total_likes')
		depth = 1
