from django.shortcuts import render
from django.views import View
from . import models


# Create your views here.
class LandingPage(View):
    def get(self, request):
        all_donations = models.Donation.objects.all()
        total_bags = 0
        for donation in all_donations:
            total_bags += donation.quantity
            print(donation.quantity)
        all_institutions = models.Institution.objects.all()
        foundations = models.Institution.objects.filter(type='Fundacja')
        non_gov_organizations = models.Institution.objects.filter(type='Organizacja Pozarządowa')
        local_collections = models.Institution.objects.filter(type='Zbiórka Lokalna')

        context = {
            'total_bags': total_bags,
            'num_of_institutions': len(all_institutions),
            'institutions': all_institutions,
            'foundations': foundations,
            'non_gov_organizations': non_gov_organizations,
            'local_collections': local_collections,

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
        return render(request, './register.html')
