
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from users import views as users_view
from articles import views as articles_view
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r"user", users_view.UserViewSet)
router.register(r"article", articles_view.ArticleViewSet)
router.register(r"get_article", articles_view.ArticleListViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
