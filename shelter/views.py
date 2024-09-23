from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    WalkScheduleForm,
    AdoptionForm,
    UserProfileForm
)
from .models import Walk, Adoption, User, Animal


class HomePageView(generic.TemplateView):
    template_name = "shelter/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_animals"] = Animal.objects.count()
        context["adopted_count"] = (
            Animal
            .objects
            .filter(status="adopted").count()
        )
        context["available_count"] = (
            Animal
            .objects
            .filter(status="available", type="dog").count()
        )

        return context


class AnimalListView(generic.ListView):
    model = Animal
    template_name = "shelter/animals_list_for_adoption.html"
    paginate_by = 6

    def get_queryset(self):
        queryset = (
            Animal
            .objects
            .filter(status="available", type__in=["cat", "dog"])
        )

        gender = self.request.GET.get("gender")
        age = self.request.GET.get("age")
        animal_type = self.request.GET.get("type")

        if gender:
            queryset = queryset.filter(gender=gender)
        if age:
            queryset = queryset.filter(age=age)
        if animal_type:
            queryset = queryset.filter(type=animal_type)

        return queryset


class OtherAnimalsListView(generic.ListView):
    model = Animal
    template_name = "shelter/other_animals_list.html"
    context_object_name = "other_animal_list"

    def get_queryset(self):
        return Animal.objects.exclude(type__in=["cat", "dog"])


class DogListView(generic.ListView):
    model = Animal
    template_name = "shelter/dog_list.html"
    paginate_by = 8

    def get_queryset(self):
        queryset = Animal.objects.filter(type="dog", status="available")
        gender = self.request.GET.get("gender")
        age = self.request.GET.get("age")

        if gender:
            queryset = queryset.filter(gender=gender)
        if age:
            queryset = queryset.filter(age=age)

        return queryset


class ScheduleWalkView(LoginRequiredMixin, generic.CreateView):
    model = Walk
    form_class = WalkScheduleForm
    template_name = "shelter/walk_schedule.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dog_pk = self.kwargs.get("dog_pk")
        context["dog"] = get_object_or_404(Animal, id=dog_pk)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.animal = self.get_context_data()["dog"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("shelter:success-walk")


class SuccessWalkView(generic.TemplateView):
    template_name = "shelter/success_walk.html"


class AnimalAdoptableDetailView(generic.DetailView):
    model = Animal
    template_name = "shelter/animal_adoptable_detail.html"


class AdoptionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Adoption
    form_class = AdoptionForm
    template_name = "shelter/adoption_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal_pk = self.kwargs.get("animal_pk")
        context["animal"] = get_object_or_404(Animal, id=animal_pk)
        return context

    def form_valid(self, form):
        animal_pk = self.kwargs.get("animal_pk")

        if Adoption.objects.filter(
            animal_id=animal_pk,
            user=self.request.user
        ).exists():
            form.add_error(
                None,
                "You have already submitted "
                "an adoption request for this animal."
            )
            return self.form_invalid(form)

        if not self.request.user.phone_number:
            form.add_error(
                None,
                "You must provide a phone number "
                "to submit your adoption request."
            )
            return self.form_invalid(form)

        form.instance.animal = get_object_or_404(Animal, id=animal_pk)
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("shelter:success-adoption")


class SuccessAdoptionView(generic.TemplateView):
    template_name = "shelter/success_adoption.html"


# view for register login and logout


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "registration/login.html"


class CustomLogoutView(LogoutView):
    template_name = "registration/logged_out.html"


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("shelter:success-registration")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


class SuccessRegistrationView(generic.TemplateView):
    template_name = "shelter/success_registration.html"


# profile

class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = "registration/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class EditProfileView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "registration/edit_profile.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('shelter:user-profile')


# articles


def article_about_cat(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "shelter/articles/article_about_cats.html"
    )


def article_about_dogs(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "shelter/articles/article_about_dogs.html"
    )


def article_about_injured_animals(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "shelter/articles/article_about_injured_animals.html"
    )


class AboutUsView(generic.TemplateView):
    template_name = "shelter/articles/about_us.html"


def help_list(request: HttpRequest) -> HttpResponse:
    return render(request, "shelter/articles/help_list.html")
