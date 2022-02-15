from django.http import HttpResponse, HttpRequest


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.path == '/health/':
            return HttpResponse('ITUscheduler is up!')

        return self.get_response(request)
