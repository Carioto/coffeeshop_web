from django.urls import path
from . import views

app_name = "pos"

urlpatterns = [
    path("", views.front_page, name="front_page"),
    path("begin", views.drinklist, name="drinklist"),
    path("<int:drink_id>", views.build, name="build"),
    path("complete", views.complete, name="complete"),
    path("changes/", views.quantities, name="quantities"),
    path("changesdone", views.changesdone, name="changesdone"),
]
