from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .serializers import ScheduleSerializer
from api.rest_api.serializers import CourseSerializer, LectureSerializer, PrerequisiteSerializer
from api.models import Course
from scheduler.models import Schedule


class ScheduleListAPIView(ListAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(user=request.user)

        #serializer = self.get_serializer(queryset, many=True)

        data = [(self.get_serializer(query).data, query) for query in queryset]
        response_data = []

        for serializer, query in data:
            serializer['courses'] = CourseSerializer(query.courses.all(), many=True).data
            response_data.append(serializer)

        for data in response_data:
            for course in data['courses']:
                query = Course.objects.get(crn=course['crn'])
                course['lectures'] = LectureSerializer(query.lecture_set.all(), many=True).data
                course['prerequisites'] = PrerequisiteSerializer(query.prerequisites.all(), many=True).data


        return Response(response_data)


class ScheduleDetailAPIView(RetrieveAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def retrieve(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            instance = self.get_object()
            serializer = self.get_serializer(instance).data

            serializer['courses'] = CourseSerializer(instance.courses.all(), many=True).data
            for data in serializer['courses']:
                query = Course.objects.get(crn=data['crn'])
                data['lectures'] = LectureSerializer(query.lecture_set.all(), many=True).data
                data['prerequisites'] = PrerequisiteSerializer(query.prerequisites.all(), many=True).data

            return Response(serializer)

        return Response({'Unauthorized attempt'}, status=HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((SessionAuthentication, ))
def course_remove(request):
    crn = int(request.data['crn'])
    schedule_id = int(request.data['schedule_id'])
    user = request.user

    schedule = get_object_or_404(Schedule, id=schedule_id)
    course = get_object_or_404(Course, crn=crn)
    if schedule.user != user and course not in schedule:
        return Response({'error': 'unauthorized attempt.'}, status=HTTP_401_UNAUTHORIZED)

    schedule.courses.remove(course)

    if len(schedule.courses.all()) == 0:
        schedule.delete()

    return Response({'success': 'Successfuly removed course {}'.format(course.crn)})

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((SessionAuthentication, ))
def course_replace(request):
    old_crn = int(request.data['old_crn'])
    new_crn = int(request.data['new_crn'])
    schedule_id = int(request.data['schedule_id'])
    user = request.user

    schedule = get_object_or_404(Schedule, id=schedule_id)
    old_course = get_object_or_404(Course, crn=old_crn)
    new_course = get_object_or_404(Course, crn=new_crn)

    if schedule.user != user and old_course not in schedule and new_course in schedule:
        return Response({'error': 'Unauthorized attempt.'}, status=HTTP_401_UNAUTHORIZED)

    schedule.courses.remove(old_course)
    schedule.courses.add(new_course)

    return Response({'success': 'Replaced {} with {}'.format(old_crn, new_crn)})



