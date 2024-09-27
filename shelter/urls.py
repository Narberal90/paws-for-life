from django.urls import path

from shelter.views import (
    HomePageView,
    help_list,
    AnimalListView,
    OtherAnimalsListView,
    AnimalAdoptableDetailView,
    DogListView,
    ScheduleWalkView,
    SuccessWalkView,
    AdoptionCreateView,
    SuccessAdoptionView,
    article_about_cat,
    article_about_dogs,
    article_about_injured_animals,
    UserProfileView,
    EditProfileView,
    AboutUsView,
    SuccessRegistrationView
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("help/", help_list, name="help-list"),
    path(
        "animals/adoptable/",
        AnimalListView.as_view(),
        name="animals-list-for-adoption"
    ),
    path(
        "animals/other-animals/",
        OtherAnimalsListView.as_view(),
        name="other-animals"
    ),
    path(
        "animal/adoptable/<int:pk>/",
        AnimalAdoptableDetailView.as_view(),
        name="animal-adoptable-detail"
    ),
    path(
        "dogs/",
        DogListView.as_view(),
        name="dog-list"
    ),
    path(
        "schedule-walk/<int:dog_pk>/",
        ScheduleWalkView.as_view(),
        name="schedule-walk"
    ),
    path(
        "adopt/<int:animal_pk>/",
        AdoptionCreateView.as_view(),
        name="adoption-create"
    ),
    path(
        "adoption-success/",
        SuccessAdoptionView.as_view(),
        name="success-adoption"
    ),
    path(
        "walk-success/",
        SuccessWalkView.as_view(),
        name="success-walk"
    ),
    path(
        "success-registration/",
        SuccessRegistrationView.as_view(),
        name="success-registration"
    ),
    path(
        "article-about-cats/",
        article_about_cat,
        name="article-about-cats"
    ),
    path(
        "article_about_dogs/",
        article_about_dogs,
        name="article-about-dogs"
    ),
    path(
        "article_about_injured_animals/",
        article_about_injured_animals,
        name="article-about-injured-animals"
    ),
    path("about/", AboutUsView.as_view(), name="about-us"),
    path(
        "user/profile/",
        UserProfileView.as_view(),
        name="user-profile"
    ),
    path(
        "user/profile/edit/",
        EditProfileView.as_view(),
        name="edit-profile"
    ),

]

app_name = "shelter"
