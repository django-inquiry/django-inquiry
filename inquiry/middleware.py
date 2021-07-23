from .models import Request

def inquiry_middleware(get_response):

    def middleware(request):
        response = get_response(request)
        req = Request()
        req.create_from_request(request, response)

        return response

    return middleware