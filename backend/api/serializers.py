from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import Article, Issue

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']



class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields='__all__'
        extra_kwargs = {"submitted_by": { "read_only":True}}
    def validate_author_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits.")
        return value
    
    
class IssueSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(source='article_id',read_only=True)
    class Meta:
        model=Issue
        fields = ['id', 'issue_title', 'vol_no', 'issue_no', 'year', 'newIssuePdf','month', 'issued_date', 'article', 'article_id']
    def validate_article_id(self, value):
        # Check if the Article with the given ID is approved
        article = Article.objects.get(id=value.id)
        if article.status != 'approved':
            raise serializers.ValidationError("The article must be approved to issue.")
        return value
    def create(self, validated_data):
        # Extract article_id from validated_data
        article_id = validated_data.pop('article_id', None)
        print(article_id.id)
        # print(validated_data.pop('article_id'))
        # Create an Issue instance
        issue = Issue.objects.create(article_id=article_id, **validated_data)
        article = Article.objects.get(id=article_id.id)
        article.status = 'published'
        article.save()
        return issue
    


from rest_framework import serializers
from .models import Reviewer

class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewer
        fields='__all__'


from .models import Announcements

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Announcements
        fields='__all__'
