from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


class RegisterFormView(FormView):
    form_class = UserCreationForm

    success_url = "/accounts/sign-in/"
    template_name = "accounts/register.html"

    def form_valid(self, form):
        form.save()

        return super(RegisterFormView, self).form_valid(form)
