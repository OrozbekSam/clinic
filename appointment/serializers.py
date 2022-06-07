from rest_framework import serializers
from . models import Appointment, AppointmentItem
# from rest_framework.validators import UniqueTogetherValidator


class AppointmentItemSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = AppointmentItem
        fields = ('doctor', 'first_name', 'last_name', 'image', 'gender', 'date_birth',
                  'body', 'phone_number', 'email', 'address', 'days', 'timeslot')
    

class AppointmentSerializer(serializers.ModelSerializer):
    positions = AppointmentItemSerializer(write_only=True, many=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'created_at', 'positions', 'status')

    def create(self, validated_data):
        doctor = validated_data.pop('positions')
        user = self.context.get('request').user
        appointment = Appointment.objects.create(user=user, status='open')

        for doc in doctor:
            doctor = doc['doctor']
            first_name = doc['first_name']
            last_name = doc['last_name']
            gender = doc['gender']
            date_birth = doc['date_birth']
            body = doc['body']
            phone_number = doc['phone_number']
            email = doc['email']
            address = doc['address']
            days = doc['days']
            timeslot = doc['timeslot']

            AppointmentItem.objects.create(appointment=appointment, doctor=doctor, first_name=first_name,
                                           last_name=last_name, gender=gender, date_birth=date_birth,
                                           body=body, phone_number=phone_number, email=email, address=address, days=days,
                                           timeslot=timeslot)
        return appointment

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['positions'] = AppointmentItemSerializer(instance.items.all(), many=True).data
        return repr
