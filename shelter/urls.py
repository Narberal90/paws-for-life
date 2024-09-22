from django.urls import path

from .views import (
    HomePageView,
    help_list,
    AnimalListView,
    OtherAnimalsListView,
    AnimalAdoptableDetailView,
    DogListView,
    ScheduleWalkView,
    SuccessView,
    AdoptionCreateView,
    SuccessAdoptionView,
    article_about_cat,
    article_about_dogs,
    article_about_injured_animals
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("help/", help_list, name="help-list"),
    path("animals/adoptable/", AnimalListView.as_view(), name="animals-list-for-adoption"),
    path("animals/other-animals/", OtherAnimalsListView.as_view(), name="other-animals"),  # Other animal in shelter
    path("animal/adoptable/<int:pk>/", AnimalAdoptableDetailView.as_view(), name="animal-adoptable-detail"),
    path('dogs/', DogListView.as_view(), name="dog-list"),
    path('schedule-walk/<int:dog_pk>/', ScheduleWalkView.as_view(), name='schedule-walk'),
    path('adopt/<int:animal_pk>/', AdoptionCreateView.as_view(), name='adoption-create'),
    path('adoption-success/', SuccessAdoptionView.as_view(), name='success-adoption'),
    path('success/', SuccessView.as_view(), name='success'),
    path('article-about-cats/', article_about_cat, name='article-about-cats'),
    path('article_about_dogs/', article_about_dogs, name='article-about-dogs'),
    path('article_about_injured_animals/', article_about_injured_animals, name='article-about-injured-animals'),
]

app_name = "shelter"
