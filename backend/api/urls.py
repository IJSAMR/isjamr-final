from django.urls import path
from api.views import ApprovedArticles, ArticleSubmitView, IssueCreateView, IssuedArticleView, ReviewerDetailView, ReviewerListCreateView,UnderReviewView,ArticleAdminView,AnnouncementListCreateView,AnnouncementDetailView
urlpatterns=[
    path("submit/",ArticleSubmitView.as_view()),
    path("under_review/",UnderReviewView.as_view()),
    path("list/",ArticleAdminView.as_view()),
    path("approve/<int:pk>/",ArticleAdminView.as_view()),
    path("create-issue/",IssueCreateView.as_view()),
    path("issues/",IssuedArticleView.as_view()),
    path("issues/<int:year>/",IssuedArticleView.as_view()),
    path("issues/<int:year>/<str:month>/",IssuedArticleView.as_view()),
    path("approved-articles/",ApprovedArticles.as_view()),
    path('reviewers/', ReviewerListCreateView.as_view(), name='reviewer-list-create'),
    path('reviewers/<int:pk>/', ReviewerDetailView.as_view(), name='reviewer-detail'),
    path('announcments/', AnnouncementListCreateView.as_view(), name='announcement-list-create'),
    path('announcments/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
]