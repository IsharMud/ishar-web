from django.core.serializers import serialize


def json_context(context=None, obj=None):
    # Include JSON-serialized content in response context.
    qs = context.get(obj)
    if qs:
        context[obj] = serialize(format="json", queryset=qs)
    return context
