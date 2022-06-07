from rest_framework import serializers
from django.db.models import Avg
from doctor.models import Doctor, Medicine, Comment, Favorite
from account.serializers import User


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        
    def is_liked(self, doctor):
        user = self.context.get('request').user
        return user.liked.filter(doctor=doctor).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['reviews_detail'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['rating'] = instance.ratings.aggregate(Avg('mark'))
        # user = self.context.get('request').user
        # if user.is_authenticated:
        #     representation['is_liked'] = self.is_liked(instance)
        representation['likes_count'] = instance.likes.count()
        return representation


class DoctorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

    def is_liked(self, doctor):
        user = self.context.get('request').user
        return user.liked.filter(doctor=doctor).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments_detail'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['comments_count'] = instance.comments.count()
        representation['rating'] = instance.ratings.aggregate(Avg('mark'))
        # print(f"******************************************{representation}")
        # print(f"############################{self.context.get('request').user}")
        # user = self.context.get('request').user
        # print(user)
        # if user.is_authenticated:
        #     representation['is_liked'] = self.is_liked(instance)
        representation['likes_count'] = instance.likes.count()
        return representation


class MedicineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Medicine
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['doctor'] = DoctorSerializer(instance.doctor.all(), many=True).data
        # user = self.context.get('request').user

        return representation


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'doctor')
        

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['doctor'] = instance.doctor.last_name
        return representation
