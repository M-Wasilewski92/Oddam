from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from . import models
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, CustomLoginForm, DonationCreationForm, IsTakenForm, \
     FirstNameChangeForm, LastNameChangeForm
from django.contrib import messages
from .models import Category, Institution, Donation
from datetime import date, datetime


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
        form = DonationCreationForm()
        context = {
            'category': category,
            'institutions': institutions,
            'form': form,
        }

        return render(request, './form.html', context)

    def post(self, request):
        form = DonationCreationForm(request.POST)
        user_onj = request.user
        if form.is_valid():
            institution = Institution.objects.get(id=form.cleaned_data['institution_id'])
            categorys = get_category_objs(form.cleaned_data['category_ids'])
            new_donation = Donation()
            new_donation.quantity = form.cleaned_data['quantity']
            new_donation.address = form.cleaned_data['address']
            new_donation.phone_number = form.cleaned_data['phone_number']
            new_donation.city = form.cleaned_data['city']
            new_donation.zip_code = form.cleaned_data['zip_code']
            new_donation.pick_up_date = form.cleaned_data['pick_up_date']
            new_donation.pick_up_time = str(form.cleaned_data['pick_up_time'])
            new_donation.pick_up_comment = form.cleaned_data['pick_up_comment']
            new_donation.institution = institution
            new_donation.user = user_onj
            new_donation.save()
            donation = Donation.objects.latest('id')
            for id in categorys:
                donation.categories.add(id)
                donation.save()
            return redirect('projectapp:donation')
        print(form.errors.as_data())
        return redirect('projectapp:add')


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


class SuccessDonation(View):

    def get(self, request):
        return render(request, './form-confirmation.html')


class UserProfile(LoginRequiredMixin, View):

    def get(self, request):
        user_donations = Donation.objects.filter(user=request.user).order_by('pick_up_date')
        form = IsTakenForm()
        context = {
            'user_donations': user_donations,
            'form': form,
        }
        return render(request, './user-page.html', context)

    def post(self, request):
        today = date.today()
        time_now = datetime.now()
        time_now = time_now.strftime("%H:%M")
        form = IsTakenForm(request.POST)
        if 'don_id' in request.POST:
            if form.is_valid():
                donation = Donation.objects.get(id=request.POST['don_id'])
                donation.is_taken = form.cleaned_data['is_taken']
                donation.pick_up_date = today
                donation.pick_up_time = time_now
                donation.save()
                return redirect('projectapp:profile')
        return render(request, './user-page.html')


class UserSettings(PasswordChangeView):
    template_name = './user-settings.html'
    success_url = reverse_lazy('projectapp:settings')
    first_name_form = FirstNameChangeForm()
    last_name_form = LastNameChangeForm()
    extra_context = {
        'first_name_form': first_name_form,
        'last_name_form': last_name_form,
    }

    def post(self, request, *args, **kwargs):
        first_name_form = FirstNameChangeForm(self.request.POST)
        if first_name_form.is_valid():
            user_new_name = User.objects.get(id=self.request.POST['user_id'])
            user_new_name.first_name = first_name_form.cleaned_data['first_name']
            user_new_name.save()
        last_name_form = LastNameChangeForm(self.request.POST)
        if last_name_form.is_valid():
            user_new_last_name = User.objects.get(id=self.request.POST['user_id'])
            user_new_last_name.last_name = last_name_form.cleaned_data['last_name']
            user_new_last_name.save()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def get_category_objs(cat_ids):
    """Recives string with ids of category objects"""
    cat_objs = []
    separated = list(cat_ids)
    for id in separated:
        cat_objs.append(int(id))
    return cat_objs
