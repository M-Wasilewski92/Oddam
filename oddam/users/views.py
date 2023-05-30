from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from .forms import (
    ContactForm,
    CustomLoginForm,
    CustomUserCreationForm,
    FirstNameChangeForm,
    LastNameChangeForm,
)
from .helpers import send_contact_mail
from .tokens import account_activation_token


class Login(View):
    def get(self, request):
        form = CustomLoginForm()
        contact_form = ContactForm()
        context = {
            "login_form": form,
            "contact_form": contact_form,
        }
        return render(request, "./login.html", context)

    def post(self, request):
        send_contact_mail(request)
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Zostałeś zalogowany jako {email}.")
                messages.info(request, f"Zostałeś zalogowany jako {email}.")
                return redirect("users:landingpage")
            else:
                messages.info(request, "Nie ma takiego użytkownika")
                return redirect("users:register")
        else:
            messages.error(request, "Błąd w formularzu")
            print(form.errors.as_data())
            return redirect("users:register")


class Register(View):
    def get(self, request):
        form = CustomUserCreationForm()
        contact_form = ContactForm()
        context = {
            "form": form,
            "contact_form": contact_form,
        }
        return render(request, "./register.html", context)

    def post(self, request):
        send_contact_mail(request)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Aktywacja Konta"
            message = render_to_string(
                "email/acc_activate_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.id)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data["email"]
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, message="Rejestracja pomyślna")
            return redirect("users:login")
        else:
            messages.error(request, "Błąd w formularzu")
            messages.error(request, form.errors)
            return redirect("users:register")


class Activate(View):
    def get(self, request, uidb64, token):
        """This function will check token, if it is valid then user will be active."""
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(
                request,
                message="Dziękuję za potwierdzenie adresu Email. Teraz możesz się zalogować.",
            )
            return redirect("users:login")

        else:
            messages.error(request, "Link Aktywacyjny jest niepoprawny")
            return redirect("users:landingpage")


class PasswordResetRequest(View):
    def get(self, request):
        password_reset_form = PasswordResetForm()
        contact_form = ContactForm()
        context = {
            "form": password_reset_form,
            "contact_form": contact_form,
        }
        return render(request, "./password_reset.html", context=context)

    def post(self, request):
        send_contact_mail(request)
        password_reset_form = PasswordResetForm(request.POST)
        contact_form = ContactForm()
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            try:
                associated_user = User.objects.get(email=data)
            except User.DoesNotExist:
                return render(
                    request,
                    "password_reset_no_user.html",
                    context={"contact_form": contact_form},
                )
            if associated_user:
                associated_user = User.objects.get(email=data)
                current_site = get_current_site(request)
                mail_subject = "Prośba o Reset hasła"
                message = render_to_string(
                    "email/password_reset_email.html",
                    {
                        "email": associated_user.email,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                        "user": associated_user,
                        "token": default_token_generator.make_token(associated_user),
                        "protocl": "http",
                    },
                )
                try:
                    send_mail(
                        subject=mail_subject,
                        message=message,
                        from_email="Mwasilewski92@gmail.com",
                        recipient_list=[associated_user.email],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    return HttpResponse("Zły Header? ")
                return redirect(
                    "/password_reset/done", context={"contact_form": contact_form}
                )


class UserSettings(PasswordChangeView):
    template_name = "./user-settings.html"
    success_url = reverse_lazy("users:settings")
    first_name_form = FirstNameChangeForm()
    last_name_form = LastNameChangeForm()
    contact_form = ContactForm()
    extra_context = {
        "first_name_form": first_name_form,
        "last_name_form": last_name_form,
        "contact_form": contact_form,
    }

    # To Do Fix Forms
    def post(self, request, *args, **kwargs):
        send_contact_mail(request)
        first_name_form = FirstNameChangeForm(self.request.POST)
        last_name_form = LastNameChangeForm(self.request.POST)
        if first_name_form.is_valid():
            if User.objects.get(id=self.request.POST["user_id"]):
                user_new_name = User.objects.get(id=self.request.POST["user_id"])
                user_new_name.first_name = first_name_form.cleaned_data["first_name"]
                user_new_name.save()
                last_name_form = LastNameChangeForm(self.request.POST)
        if last_name_form.is_valid():
            user_new_last_name = User.objects.get(id=self.request.POST["user_id"])
            user_new_last_name.last_name = last_name_form.cleaned_data["last_name"]
            user_new_last_name.save()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
