from django.utils.cache import patch_cache_control
from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):

    def process_response(self, request, response):

        # for further versions of django we can use add_never_cache_headers(response) instead
        patch_cache_control(response, no_cache=True, no_store=True)
        
        return response
