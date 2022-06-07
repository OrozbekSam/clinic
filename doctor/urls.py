from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views
router = SimpleRouter()
router.register('doctors', views.DoctorViewSet)
router.register('categories', views.MedicineViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('reviews/', views.CommentListCreateView.as_view()),
    path('reviews/<int:pk>/', views.CommentDetailView.as_view()),
    path('favorites/', views.UserFavoriteList.as_view()),
]
