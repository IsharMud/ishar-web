from django.conf import settings


def admin_email(request):
    # Context processor for administrator e-mail address.
    return {"ADMIN_EMAIL": settings.DEFAULT_FROM_EMAIL}


def website_title(request):
    # Context processor for website title.
    return {"WEBSITE_TITLE": settings.WEBSITE_TITLE}
