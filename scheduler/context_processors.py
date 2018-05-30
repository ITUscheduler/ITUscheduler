from api.models import MajorCode


def global_processor(request):
    return {"major_codes": MajorCode.objects.all()}
