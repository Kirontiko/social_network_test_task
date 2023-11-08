from django.utils import timezone


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_anonymous:
            user = request.user
            user.last_request = timezone.now()
            user.save()

        return response
