from rest_framework import serializers

from course.models import Course, Lesson


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
