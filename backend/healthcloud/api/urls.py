from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = DefaultRouter()
router.register("recordings", views.RecordingViewSet, basename="recordings")

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("reports/", views.ListReportsView.as_view(), name="reports"),
    path(
        "recordings/upload/",
        views.UploadRecordingView.as_view(),
        name="upload_recording",
    ),
]

urlpatterns += router.urls
