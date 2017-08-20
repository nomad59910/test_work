from django.conf.urls import url
from django.contrib.auth.views import login, logout
from .views import RegisterFormView

app_name = 'accounts'

urlpatterns = [
    url(r'^sign-in', login, {'template_name':'accounts/login.html',},
        name='login'),
    url(r'^logout$', logout, {'next_page': 'task:tasks', }, name='logout'),
    url(r'^register$', RegisterFormView.as_view(), name="register"),
]
