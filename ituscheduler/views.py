from django.http import (
    HttpResponse,
    HttpRequest,
)


def empty(request: HttpRequest):
    return HttpResponse("")
