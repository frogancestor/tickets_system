from .models import AutorizatedPeople
from datetime import date, timedelta
from .views import autorisation_view


def auth_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if request.path != '/auth' and 'admin' not in request.path:
            try:
                tokenToCheck = AutorizatedPeople.objects.get(token=request.COOKIES.get('auth_token'))
            except:
                response = autorisation_view(request)
            else:
                if (tokenToCheck.expiration_date) - date.today() <= timedelta(days=0):
                    tokenToCheck.delete()
                    response = autorisation_view(request)
        return response
    return middleware
