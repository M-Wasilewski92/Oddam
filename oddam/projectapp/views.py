from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from . import models
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib import messages

from .models import Category, Institution


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


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        category = Category.objects.all()
        institutions = Institution.objects.all()

        context = {
            'category': category,
            'institutions': institutions,
        }

        return render(request, './form.html', context)


class Login(View):
    def get(self, request):
        form = CustomLoginForm()
        context = {
            'login_form': form
        }
        return render(request, './login.html', context)

    def post(self, request):
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Zostałeś zalogowany jako {email}.")
                return redirect('projectapp:landingpage')
            else:
                messages.info(request, 'Nie ma takiego użytkownika')
                return redirect('projectapp:register')
        else:
            messages.error(request, 'Błąd w formularzu')
            return redirect('projectapp:register')


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
            return redirect('projectapp:register')
