from django.shortcuts import get_object_or_404,get_list_or_404
from django.contrib.auth import get_user_model
from requests import Response
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView
from api.models import Article, Issue
from api.serializers import ArticleSerializer, IssueSerializer
from api.utils import send_article_sibmission_mail
from .permissions import IsAdminOrCreateOnly, IsAdminUser
from rest_framework_simplejwt.views import TokenRefreshView


#view for obtaining token pair for admin user ie is_staff==true an editor of the journel

class AdminTokenObtainPairView(TokenObtainPairView):


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.user

        if not user.is_staff:  # Check if the user is an admin
            return Response({'detail': 'Admin access only'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)
    




class VerifyAdminView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        return Response({'detail': 'User is an admin.'})



class AdminTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh['user_id']
            User = get_user_model()
            user = User.objects.get(id=user_id)
        except Exception as e:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_staff:
            return Response({"detail": "Admin access only."}, status=status.HTTP_403_FORBIDDEN)

        data = {
            'access': str(refresh.access_token),
        }

        return Response(data, status=status.HTTP_200_OK)



#view to create an article

class ArticleSubmitView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        article= serializer.save(submitted_by=self.request.user,status='submitted')
        send_article_sibmission_mail(article.author_email,article.author_name,article.title,article.submitted_date)

#views to get all articles under review and approved and submitted
class UnderReviewView(ListAPIView):

    queryset=Article.objects.exclude(status__in = ['rejected','published'])
    serializer_class=ArticleSerializer
    permission_classes=[IsAuthenticated]


#view to approve an article

class ArticleAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk=None):
        if pk:
            article = get_object_or_404(Article, pk=pk)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        else:
            articles = Article.objects.all()
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data)

    def patch(self, request, pk=None):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        try:
            article = Article.objects.get(pk=pk)
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



# views for issues
#view to create a issue

class IssueCreateView(ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class=IssueSerializer
    permission_classes=[IsAdminUser]
    def perform_create(self, serializer):
        # Modify a particular value before saving
        instance = serializer.save()

        instance.month = instance.month.lower()  # Change 'some_field' to the field you want to modify
        instance.save()

#view to view all issued article

class IssuedArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year=None,month=None):
        if year and month:
            articles = Issue.objects.filter(year=year,month=month) 
            if not articles.exists():
                return Response({"detail": "No issues found for the specified year and month."}, status=204)
        elif(year):
            articles = Issue.objects.filter(year=year)
            if not articles.exists():
                return Response({"details: no issue found on the month"})
            
        else:
            articles = Issue.objects.all() 
        serializer = IssueSerializer(articles, many=True)
        return Response(serializer.data)

class ApprovedArticles(ListAPIView):
    permission_classes=[IsAdminUser]
    queryset=Article.objects.filter(status="approved")
    serializer_class=ArticleSerializer


class ArticleCountView():
    pass

# views.py

from rest_framework import generics
# from rest_framework.permissions import IsAdminUser
from .models import Reviewer
from .serializers import ReviewerSerializer

class ReviewerListCreateView(generics.ListCreateAPIView):
    queryset = Reviewer.objects.all()
    serializer_class = ReviewerSerializer
    # permission_classes = [IsAdminUser]

class ReviewerDetailView(generics.RetrieveDestroyAPIView):
    queryset = Reviewer.objects.all()
    serializer_class = ReviewerSerializer
    permission_classes = [IsAdminUser]


#aanoucemnts

from .models import Announcements
from .serializers import AnnouncementSerializer

class AnnouncementListCreateView(generics.ListCreateAPIView):
    queryset = Announcements.objects.all()
    serializer_class = AnnouncementSerializer
    # permission_classes = [IsAdminUser]

class AnnouncementDetailView(generics.RetrieveDestroyAPIView):
    queryset = Announcements.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminUser]