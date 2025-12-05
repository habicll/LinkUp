from django.http import HttpResponse


class CorsMiddleware:
    """
    Simple CORS middleware that:
    - returns a short-circuit response for OPTIONS preflight requests
    - echoes the Origin header (safer when using credentials)
    - sets common CORS headers and reflects requested headers/methods

    This middleware is intentionally conservative and compatible with
    django-cors-headers (if you decide to use that package, prefer its
    middleware and place it near the top of MIDDLEWARE).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def _get_origin(self, request):
        # Prefer the Origin header (standard for CORS). Fallback to Referer if needed.
        origin = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER')
        return origin

    def _set_cors_headers(self, response, origin, request):
        if origin:
            # Echo origin instead of using '*' so credentials are allowed by browsers
            response['Access-Control-Allow-Origin'] = origin
            response['Vary'] = 'Origin'
            response['Access-Control-Allow-Credentials'] = 'true'
        else:
            response['Access-Control-Allow-Origin'] = '*'

        # Default allowed methods and headers
        response.setdefault('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')

        # If the browser sent a preflight request with Access-Control-Request-Headers,
        # reflect them back so custom headers are allowed.
        acrh = request.META.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS')
        if acrh:
            response['Access-Control-Allow-Headers'] = acrh
        else:
            response.setdefault('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')

        # Expose some headers to the client (optional)
        response.setdefault('Access-Control-Expose-Headers', 'Content-Length, Content-Range, Authorization')

        # Cache preflight for 1 day
        response.setdefault('Access-Control-Max-Age', '86400')

    def __call__(self, request):
        origin = self._get_origin(request)

        # Handle preflight OPTIONS: short-circuit and return the correct headers
        if request.method == 'OPTIONS':
            response = HttpResponse(status=204)
            self._set_cors_headers(response, origin, request)
            return response

        # Normal request: call the view then add CORS headers to the response
        response = self.get_response(request)
        self._set_cors_headers(response, origin, request)
        return response