from rest_framework import serializers
from django.conf import settings

from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        student_count = len(data.get('students'))
        if student_count > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError(f'Не более {settings.MAX_STUDENTS_PER_COURSE} студентов на курс!')
        return data
