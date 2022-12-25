from django.urls import path

from . import views

app_name = "Carbon"

urlpatterns = [
    path(
        "<str:Depart>",
        views.CarbonEmissionQuery.as_view(),
    ),
]
