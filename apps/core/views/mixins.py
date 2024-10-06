from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic.base import View


@method_decorator(never_cache, name="dispatch")
class NeverCacheMixin(View):
    pass
