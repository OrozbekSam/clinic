from appointment.views import AppointmentItemListView, CreateAppointmentView, UserAppointmentList, UpdateAppointmentsStatusView
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Clinic project API",
      default_version='v1',
      description="This is test blog project.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('doctor.urls')),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/appoints/', AppointmentItemListView.as_view()),
    path('api/v1/appointments/', CreateAppointmentView.as_view()),
    path('api/v1/appointments/own/', UserAppointmentList.as_view()),
    path('api/v1/appointments/<int:pk>/', UpdateAppointmentsStatusView.as_view()),
    path('api/v1/rp/', include('rating.urls')),
    path('', include('chat.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
