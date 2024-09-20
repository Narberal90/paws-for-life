from django.urls import path

from .views import HomePageView, AnimalTypeListView, AnimalTypeDetailView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("animal-types/", AnimalTypeListView.as_view(), name="animal-type-list"),
    path("animal-types/<int:pk>/", AnimalTypeDetailView.as_view(), name="animal-type-detail"),
]

app_name = "shelter"
