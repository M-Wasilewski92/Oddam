from django.shortcuts import render, redirect
from django.views import View, generic
from . import models
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.forms import ValidationError

# Create your views here.
class LandingPage(View):
    def get(self, request):
        all_donations = models.Donation.objects.all()
        total_bags = 0
        for donation in all_donations:
            total_bags += donation.quantity

        all_institutions = models.Institution.objects.all()
        # Institution by Foundations whit pagination
        foundations = models.Institution.objects.filter(type='Fundacja')
        paginate_foundations = Paginator(foundations, 5)
        page_for_foundations = request.GET.get('slide1')
        foundation_page = paginate_foundations.get_page(page_for_foundations)
        # Institution by No gov organizations whit pagination
        non_gov_organizations = models.Institution.objects.filter(type='Organizacja Pozarządowa')
        paginate_no_gov = Paginator(non_gov_organizations, 5)
        page_for_no_gov = request.GET.get('slide2')
        no_gov_page = paginate_no_gov.get_page(page_for_no_gov)
        # Institution by local collections whit pagination
        local_collections = models.Institution.objects.filter(type='Zbiórka Lokalna')
        paginate_collections = Paginator(local_collections, 5)
        page_for_collections = request.GET.get('slide3')
        print(page_for_collections)
        collections_page = paginate_collections.get_page(page_for_collections)

        context = {
            'total_bags': total_bags,
            'num_of_institutions': len(all_institutions),
            'institutions': all_institutions,
            'foundations_page': foundation_page,
            'no_gov': no_gov_page,
            'collections_page': collections_page,

        }
        return render(request, './index.html', context=context)


class AddDonation(View):
    def get(self, request):
        return render(request, './form.html')


class Login(View):
    def get(self, request):
        return render(request, './login.html')


class Register(View):

    def get(self, request):
        form = CustomUserCreationForm()
        context = {
            'form': form
        }
        return render(request, './register.html', context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Rejestracja zakończona")
            return redirect('projectapp:login')

        else:
            messages.error(request, 'Błąd w formularzu')
            print('SHIT')
            raise ValidationError("Hasła muszą pasować do siebie")
            return redirect('projectapp:register')
