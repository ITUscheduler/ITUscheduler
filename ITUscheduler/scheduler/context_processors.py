from api.models import CourseCode


def global_processor(request):
    return {"course_codes": CourseCode.objects.all()}
