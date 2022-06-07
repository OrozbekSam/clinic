from . import views
from django.urls import path


urlpatterns = [
    path('rating/', views.RatingCreateApiView.as_view()),
    path('drugstore/', views.ParsingView.as_view()),

]
