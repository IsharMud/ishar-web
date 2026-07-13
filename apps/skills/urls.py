from django.urls import path

from .views import SkillDetailView, SkillIndexView


urlpatterns = [
    path("", SkillIndexView.as_view(), name="skills"),
    path("<str:skill_name>/", SkillDetailView.as_view(), name="skill_page"),
]
