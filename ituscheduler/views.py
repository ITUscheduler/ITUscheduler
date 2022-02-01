from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def health_check(request: HttpRequest):
    return HttpResponse("ITUscheduler is up!")
