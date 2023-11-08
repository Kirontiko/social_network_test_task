from django.urls import path, include
from rest_framework.routers import DefaultRouter

from post.views import PostViewSet, AnalyticsViewSet

app_name = "post"
router = DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("analytics/", AnalyticsViewSet.as_view({"get": "list"})),
]
