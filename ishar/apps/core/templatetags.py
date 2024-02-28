from django.template.defaulttags import register


@register.filter(name="get_dict_item")
def get_dict_item(dictionary, key):
    return dictionary.get(key)
