def get_category_objs(cat_ids):
    """Recives string with ids of category objects."""
    cat_objs = []
    separated = list(cat_ids)
    for id in separated:
        cat_objs.append(int(id))
    return cat_objs


def send_contact_mail(request):
    """Function will send Contact  Form Emial to Admins."""
    admins = User.objects.filter(is_superuser=True)
    contact_form = ContactForm(request.POST)
    if contact_form.is_valid():
        subject = "Kontakt"
        body = {
            "first_name": contact_form.cleaned_data["first_name"],
            "last_name": contact_form.cleaned_data["last_name"],
            "message": contact_form.cleaned_data["message"],
        }
        message = "\n".join(body.values())

        try:
            for admin in admins:
                # Currently sends mail to same email
                send_mail(
                    subject,
                    message,
                    os.environ.get("EMAIL_HOST_USER"),
                    [os.environ.get("EMAIL_HOST_USER")],
                )  # [f'{admin.email}'])
        except BadHeaderError:
            return HttpResponse("Zły Header? ")
        return redirect("projectapp:landingpage")
    return None
