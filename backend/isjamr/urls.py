from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from api.views import AdminTokenObtainPairView, AdminTokenRefreshView, VerifyAdminView
from django.conf import settings

urlpatterns = [
    path('api/v1/super-admin/', admin.site.urls),
    path("api/v1/auth/",include("djoser.urls")),
    path("api/v1/auth/",include("djoser.urls.jwt")),
    path("api/v1/verify-admin/",VerifyAdminView.as_view(),name="verify-admin"), 
    path("api/v1/auth/admin/",AdminTokenObtainPairView.as_view(),name="admin-auth"), #admin login
    path("api/v1/auth/admin/token/refresh/",AdminTokenRefreshView.as_view(),name="refresh-admin"), #admin token refresh
    path("api/v1/article/",include("api.urls")),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
