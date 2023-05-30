from datetime import date, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import View

from .forms import ContactForm, DonationCreationForm, IsTakenForm
from .helpers import get_category_objs, send_contact_mail
from .models import Category, Donation, Institution


# Create your views here.
class LandingPage(View):
    def get(self, request):
        all_donations = Donation.objects.all()
        total_bags = 0
        for donation in all_donations:
            total_bags += donation.quantity
        # Institution data to display.
        all_institutions = Institution.objects.all()
        # Institution by Foundations whit pagination
        foundations = Institution.objects.filter(type="Fundacja").order_by("id")
        paginate_foundations = Paginator(foundations, 5)
        page_for_foundations = request.GET.get("slide1")
        foundation_page = paginate_foundations.get_page(page_for_foundations)
        # Institution by No gov organizations whit pagination
        non_gov_organizations = Institution.objects.filter(
            type="Organizacja Pozarządowa"
        ).order_by("id")
        paginate_no_gov = Paginator(non_gov_organizations, 5)
        page_for_no_gov = request.GET.get("slide2")
        no_gov_page = paginate_no_gov.get_page(page_for_no_gov)
        # Institution by local collections whit pagination
        local_collections = Institution.objects.filter(type="Zbiórka Lokalna").order_by(
            "id"
        )
        paginate_collections = Paginator(local_collections, 5)
        page_for_collections = request.GET.get("slide3")
        collections_page = paginate_collections.get_page(page_for_collections)
        contact_form = ContactForm()
        context = {
            "total_bags": total_bags,
            "num_of_institutions": len(all_institutions),
            "institutions": all_institutions,
            "foundations_page": foundation_page,
            "no_gov": no_gov_page,
            "collections_page": collections_page,
            "contact_form": contact_form,
        }
        return render(request, "./index.html", context=context)

    def post(self, request):
        send_contact_mail(request)
        return redirect("projectapp:landingpage")


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        category = Category.objects.all()
        institutions = Institution.objects.all()
        form = DonationCreationForm()
        contact_form = ContactForm()
        context = {
            "category": category,
            "institutions": institutions,
            "form": form,
            "contact_form": contact_form,
        }

        return render(request, "./form.html", context)

    def post(self, request):
        send_contact_mail(request)
        form = DonationCreationForm(request.POST)
        user_onj = request.user
        if form.is_valid():
            institution = Institution.objects.get(
                id=form.cleaned_data["institution_id"]
            )
            categorys = get_category_objs(form.cleaned_data["category_ids"])
            new_donation = Donation()
            new_donation.quantity = form.cleaned_data["quantity"]
            new_donation.address = form.cleaned_data["address"]
            new_donation.phone_number = form.cleaned_data["phone_number"]
            new_donation.city = form.cleaned_data["city"]
            new_donation.zip_code = form.cleaned_data["zip_code"]
            new_donation.pick_up_date = form.cleaned_data["pick_up_date"]
            new_donation.pick_up_time = str(form.cleaned_data["pick_up_time"])
            new_donation.pick_up_comment = form.cleaned_data["pick_up_comment"]
            new_donation.institution = institution
            new_donation.user = user_onj
            new_donation.save()
            donation = Donation.objects.latest("id")
            for id in categorys:
                donation.categories.add(id)
                donation.save()
            return redirect("projectapp:donation")
        print(form.errors.as_data())
        return redirect("projectapp:add")


class SuccessDonation(View):
    def get(self, request):
        contact_form = ContactForm()
        return render(
            request, "./form-confirmation.html", context={"contact_form": contact_form}
        )


class UserProfile(LoginRequiredMixin, View):
    def get(self, request):
        user_donations = Donation.objects.filter(user=request.user).order_by(
            "pick_up_date"
        )
        form = IsTakenForm()
        contact_form = ContactForm()
        context = {
            "user_donations": user_donations,
            "form": form,
            "contact_form": contact_form,
        }
        return render(request, "./user-page.html", context)

    def post(self, request):
        send_contact_mail(request)
        today = date.today()
        time_now = datetime.now()
        time_now = time_now.strftime("%H:%M")
        form = IsTakenForm(request.POST)
        if "don_id" in request.POST:
            if form.is_valid():
                donation = Donation.objects.get(id=request.POST["don_id"])
                donation.is_taken = form.cleaned_data["is_taken"]
                donation.pick_up_date = today
                donation.pick_up_time = time_now
                donation.save()
                return redirect("projectapp:profile")
        return redirect("projectapp:profile")
