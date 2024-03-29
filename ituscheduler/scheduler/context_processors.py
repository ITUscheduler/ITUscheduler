from ..api.models import (
    MajorCode,
    Semester,
)


def global_processor(request):
    return {
        "major_codes": MajorCode.objects.all(),
        "semesters": [Semester.objects.current()],
        "current_semester": Semester.objects.current()
    }
