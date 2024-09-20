from django.views import generic

from shelter.models import Animal, AnimalType


class HomePageView(generic.TemplateView):
    template_name = "shelter/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_animals"] = Animal.objects.count()
        context["adopted_count"] = Animal.objects.filter(status="adopted").count()
        return context


class AnimalTypeListView(generic.ListView):
    model = AnimalType
    template_name = "shelter/animal_type_list.html"
    context_object_name = "animal_type_list"


class AnimalTypeDetailView(generic.DetailView):
    model = AnimalType
    template_name = "shelter/animal_type_detail.html"
    context_object_name = "animal_type_detail"