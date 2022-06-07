from rest_framework import generics, permissions, status as st
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from . models import Appointment


class AppointmentItemListView(generics.ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = serializers.AppointmentSerializer


class CreateAppointmentView(generics.CreateAPIView):
    serializer_class = serializers.AppointmentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserAppointmentList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        appointments = user.appointments.all()
        serializer = serializers.AppointmentSerializer(appointments, many=True).data
        return Response(serializer)


class UpdateAppointmentsStatusView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def patch(self, request, pk):
        status = request.data['status']
        if status not in ['in_check', 'closed']:
            return Response('Invalid Status', status=st.HTTP_400_BAD_REQUEST)
        appointment = Appointment.objects.get(pk=pk)
        appointment.status = status
        appointment.save()
        serializer = serializers.AppointmentSerializer(appointment)
        return Response(serializer.data, status=st.HTTP_206_PARTIAL_CONTENT)
