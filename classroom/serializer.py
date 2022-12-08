from rest_framework import serializers
from teacher.models import Subject
from teacher.serializers import SubjectSerializer
from .models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    classroom_id = serializers.UUIDField(read_only=True)
    subject = SubjectSerializer()
    # class_total_amount = serializers.DecimalField(max_digits=5,  decimal_places=1, read_only=True)

    class Meta:
        model = Classroom
        # fields = '__all__'
        exclude = ['students']


class ClassroomCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = ['title', 'description', 'subject', 'class_date']


class EmptySerializer(serializers.Serializer):
    pass